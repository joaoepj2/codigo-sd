"""
monitor.py — Painel Rich de monitoramento de IPC em tempo real.

Conecta ao broker na porta :5556 e atualiza o terminal com:
  • Tabela de status de cada worker (msgs, erros, latência)
  • Log rolante das últimas mensagens
  • Barra de saúde do sistema
  • Alertas de erros e workers offline

Uso:
    python monitor.py [--host 127.0.0.1] [--port 5556]

Dependências:
    pip install rich
"""

import socket
import json
import threading
import argparse
import time
import collections
from datetime import datetime

from rich.console     import Console
from rich.table       import Table
from rich.panel       import Panel
from rich.layout      import Layout
from rich.live        import Live
from rich.text        import Text
from rich.columns     import Columns
from rich.rule        import Rule
from rich.align       import Align
from rich             import box

# ── Configuração ─────────────────────────────────────────────────
MAX_LOG_VISIBLE = 18   # linhas de log mostradas no painel
REFRESH_HZ      = 4    # atualizações por segundo

console = Console()

# ── Estado local (atualizado pelas threads de socket) ─────────────
state_lock   = threading.Lock()
process_data: dict = {}        # worker_id → stats
message_log: collections.deque = collections.deque(maxlen=200)
alerts: collections.deque      = collections.deque(maxlen=5)
connected  = False
total_msgs = 0
total_errs = 0


# ════════════════════════════════════════════════════════════════
#  Funções de renderização Rich
# ════════════════════════════════════════════════════════════════

def build_header() -> Panel:
    agora = datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
    status_txt = ("CONECTADO", "bold green")  if connected else ("DESCONECTADO", "bold red")
    header = Text.assemble(
        ("  IPC Monitor  ", "bold white on #1e1e2e"),
        "   ",
        status_txt,
        "   ",
        (f"{agora}", "dim"),
    )
    return Panel(Align.center(header), style="bold", padding=(0, 1))


def build_process_table() -> Panel:
    t = Table(
        box=box.ROUNDED,
        show_header=True,
        header_style="bold cyan",
        border_style="dim",
        expand=True,
        row_styles=["", "dim"],
    )
    t.add_column("Worker",    style="bold",       min_width=9)
    t.add_column("Endereço",  style="dim",        min_width=16)
    t.add_column("Status",                        min_width=10)
    t.add_column("Msgs",      justify="right",    min_width=7)
    t.add_column("Erros",     justify="right",    min_width=7)
    t.add_column("Últ. msg",  style="dim",        min_width=10)
    t.add_column("Saúde",                         min_width=20)

    with state_lock:
        dados = dict(process_data)

    if not dados:
        t.add_row("—", "aguardando workers...", "", "", "", "", "")
    else:
        for wid in sorted(dados):
            s = dados[wid]
            status = s.get("status", "?")
            msgs   = s.get("msgs",   0)
            erros  = s.get("erros",  0)
            total  = msgs + erros or 1
            taxa_ok = msgs / total

            # Barra de saúde proporcional
            barra_w = 16
            cheio   = int(barra_w * taxa_ok)
            vazio   = barra_w - cheio
            if taxa_ok > 0.9:
                cor = "green"
            elif taxa_ok > 0.7:
                cor = "yellow"
            else:
                cor = "red"
            barra = Text()
            barra.append("█" * cheio, style=cor)
            barra.append("░" * vazio, style="dim")
            barra.append(f" {taxa_ok*100:.0f}%", style=f"bold {cor}")

            # Cor do contador de erros
            erros_txt = Text(str(erros))
            erros_txt.stylize("bold red" if erros > 0 else "dim")

            t.add_row(
                wid,
                s.get("addr", "—"),
                status,
                str(msgs),
                erros_txt,
                s.get("last_seen", "—"),
                barra,
            )

    return Panel(t, title="[bold]Processos[/]", border_style="cyan", padding=(0, 1))


def _tipo_style(tipo: str) -> tuple[str, str]:
    mapa = {
        "task":   ("📋", "cyan"),
        "result": ("✅", "green"),
        "error":  ("❌", "bold red"),
    }
    return mapa.get(tipo, ("💬", "white"))


def build_log_panel() -> Panel:
    linhas: list[Text] = []
    with state_lock:
        entradas = list(message_log)[-MAX_LOG_VISIBLE:]

    for e in reversed(entradas):
        icone, cor = _tipo_style(e.get("type", ""))
        linha = Text()
        linha.append(f" {e.get('time','')}", style="dim")
        linha.append(f"  {icone} ", )
        linha.append(f"{e.get('worker_id','?'):>10}", style=f"bold {cor}")
        linha.append("  ")
        linha.append(e.get("payload", ""), style=cor)
        linhas.append(linha)

    # Preenche linhas vazias para manter altura fixa
    while len(linhas) < MAX_LOG_VISIBLE:
        linhas.append(Text(""))

    conteudo = Text("\n").join(linhas)
    return Panel(conteudo, title="[bold]Log de mensagens[/]",
                 border_style="green", padding=(0, 1))


def build_summary() -> Panel:
    with state_lock:
        n_workers = len(process_data)
        online    = sum(1 for s in process_data.values() if "online" in s.get("status",""))
        t_msgs    = total_msgs
        t_errs    = total_errs

    taxa = (t_msgs / (t_msgs + t_errs) * 100) if (t_msgs + t_errs) else 100.0

    items = [
        Panel(
            Align.center(Text.assemble(
                (f"{n_workers}", "bold white"), ("\nworkers", "dim")
            )),
            style="blue", padding=(0, 2),
        ),
        Panel(
            Align.center(Text.assemble(
                (f"{online}", "bold green"), ("\nonline", "dim")
            )),
            style="green", padding=(0, 2),
        ),
        Panel(
            Align.center(Text.assemble(
                (f"{t_msgs}", "bold cyan"), ("\nmensagens", "dim")
            )),
            style="cyan", padding=(0, 2),
        ),
        Panel(
            Align.center(Text.assemble(
                (f"{t_errs}", "bold red" if t_errs else "dim"), ("\nerros", "dim")
            )),
            style="red" if t_errs else "dim", padding=(0, 2),
        ),
        Panel(
            Align.center(Text.assemble(
                (f"{taxa:.1f}%", "bold green" if taxa > 90 else "bold yellow"),
                ("\nsucesso", "dim")
            )),
            style="green" if taxa > 90 else "yellow", padding=(0, 2),
        ),
    ]
    return Panel(Columns(items, equal=True, expand=True),
                 title="[bold]Resumo[/]", border_style="white", padding=(0, 0))


def build_alerts() -> Panel:
    with state_lock:
        lista = list(alerts)

    if not lista:
        txt = Text("  Nenhum alerta  ", style="dim")
    else:
        linhas = []
        for a in reversed(lista):
            linhas.append(Text.assemble(
                (f" {a['time']} ", "dim"),
                ("⚠ ", "bold yellow"),
                (a["msg"], "yellow"),
            ))
        txt = Text("\n").join(linhas)

    return Panel(txt, title="[bold yellow]Alertas[/]",
                 border_style="yellow", padding=(0, 1))


def render() -> Layout:
    layout = Layout()
    layout.split_column(
        Layout(build_header(),        name="header",  size=3),
        Layout(build_summary(),       name="summary", size=6),
        Layout(name="main",           ratio=1),
        Layout(name="bottom",         ratio=1),
    )
    layout["main"].split_row(
        Layout(build_process_table(), name="tabela", ratio=4),

    )
    layout["bottom"].split_row(
        Layout(build_log_panel(),     name="log",    ratio=3),
        Layout(build_alerts(),        name="alerts", ratio=2),
    )

    return layout


# ════════════════════════════════════════════════════════════════
#  Thread de recepção de dados do broker
# ════════════════════════════════════════════════════════════════

def receive_loop(host: str, port: int):
    global connected, total_msgs, total_errs
    buf = ""
    while True:
        try:
            with socket.create_connection((host, port), timeout=5) as conn:
                connected = True
                while True:
                    chunk = conn.recv(8192).decode(errors="replace")
                    if not chunk:
                        break
                    buf += chunk
                    while "\n" in buf:
                        line, buf = buf.split("\n", 1)
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            pkt = json.loads(line)
                        except json.JSONDecodeError:
                            continue

                        event = pkt.get("event")
                        data  = pkt.get("data", {})

                        with state_lock:
                            if event == "snapshot":
                                process_data.update(data.get("stats", {}))
                                for entry in data.get("log", []):
                                    message_log.append(entry)
                                    if entry.get("type") == "error":
                                        total_errs += 1
                                    else:
                                        total_msgs += 1

                            elif event == "stats":
                                process_data.update(data)
                                # Alerta workers offline
                                for wid, s in data.items():
                                    if "offline" in s.get("status", ""):
                                        alerts.append({
                                            "time": datetime.now().strftime("%H:%M:%S"),
                                            "msg":  f"{wid} ficou offline",
                                        })

                            elif event == "message":
                                message_log.append(data)
                                if data.get("type") == "error":
                                    total_errs += 1
                                    alerts.append({
                                        "time": datetime.now().strftime("%H:%M:%S"),
                                        "msg":  f"{data.get('worker_id')} — {data.get('payload')}",
                                    })
                                else:
                                    total_msgs += 1

        except (ConnectionRefusedError, OSError, TimeoutError):
            connected = False
            time.sleep(2)


# ════════════════════════════════════════════════════════════════
#  Ponto de entrada
# ════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="Monitor Rich de IPC via sockets")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5556)
    args = parser.parse_args()

    # Thread de dados em background
    t = threading.Thread(target=receive_loop, args=(args.host, args.port), daemon=True)
    t.start()

    console.print(Rule("[bold cyan]IPC Monitor[/] iniciando..."))
    time.sleep(0.5)

    try:
        with Live(render(), console=console, refresh_per_second=REFRESH_HZ,
                  screen=True) as live:
            while True:
                live.update(render())
                time.sleep(1 / REFRESH_HZ)
    except KeyboardInterrupt:
        console.print("\n[bold yellow]Monitor encerrado.[/]")


if __name__ == "__main__":
    main()
