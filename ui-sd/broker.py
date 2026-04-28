"""
broker.py — Roteador central de mensagens via sockets TCP.

Expõe duas portas:
  :5555  — workers conectam e enviam mensagens JSON
  :5556  — monitor conecta e recebe estatísticas + mensagens

Uso:
    python broker.py
"""

import socket
import threading
import json
import time
import collections
from datetime import datetime

# ── Configurações ────────────────────────────────────────────────
HOST          = "127.0.0.1"
PORT_WORKERS  = 5555   # workers falam aqui
PORT_MONITOR  = 5556   # monitor escuta aqui
MAX_LOG       = 200    # máx. de mensagens no histórico

# ── Estado compartilhado ─────────────────────────────────────────
lock          = threading.Lock()
message_log   = collections.deque(maxlen=MAX_LOG)   # histórico de msgs
process_stats = {}   # {worker_id: {msgs, erros, last_seen, status}}
monitor_conns = []   # sockets de monitores conectados


def ts() -> str:
    return datetime.now().strftime("%H:%M:%S")


def broadcast_to_monitors(payload: dict):
    """Envia JSON para todos os monitores conectados."""
    data = (json.dumps(payload) + "\n").encode()
    dead = []
    with lock:
        for conn in monitor_conns:
            try:
                conn.sendall(data)
            except OSError:
                dead.append(conn)
        for conn in dead:
            monitor_conns.remove(conn)


def handle_worker(conn: socket.socket, addr):
    """Thread que trata um worker conectado na porta :5555."""
    worker_id = None
    buf = ""
    try:
        while True:
            chunk = conn.recv(4096).decode(errors="replace")
            if not chunk:
                break
            buf += chunk
            while "\n" in buf:
                line, buf = buf.split("\n", 1)
                line = line.strip()
                if not line:
                    continue
                try:
                    msg = json.loads(line)
                except json.JSONDecodeError:
                    continue

                worker_id = msg.get("worker_id", str(addr))
                kind      = msg.get("type", "msg")
                payload   = msg.get("payload", "")

                # Atualiza estatísticas do worker
                with lock:
                    if worker_id not in process_stats:
                        process_stats[worker_id] = {
                            "msgs": 0, "erros": 0,
                            "last_seen": ts(), "status": "🟢 online",
                            "addr": f"{addr[0]}:{addr[1]}",
                        }
                    s = process_stats[worker_id]
                    s["last_seen"] = ts()
                    s["status"]    = "🟢 online"
                    if kind == "error":
                        s["erros"] += 1
                    else:
                        s["msgs"] += 1

                # Registra no log
                entry = {
                    "time":      ts(),
                    "worker_id": worker_id,
                    "type":      kind,
                    "payload":   str(payload)[:120],
                }
                with lock:
                    message_log.append(entry)

                # Notifica monitores
                broadcast_to_monitors({"event": "message", "data": entry})
                broadcast_to_monitors({
                    "event": "stats",
                    "data":  dict(process_stats),
                })

    finally:
        if worker_id:
            with lock:
                if worker_id in process_stats:
                    process_stats[worker_id]["status"] = "🔴 offline"
            broadcast_to_monitors({
                "event": "stats",
                "data":  dict(process_stats),
            })
        conn.close()


def handle_monitor(conn: socket.socket):
    """Thread que mantém conexão de um monitor na porta :5556."""
    with lock:
        monitor_conns.append(conn)
        # Envia snapshot inicial
        snapshot = {
            "event": "snapshot",
            "data": {
                "stats": dict(process_stats),
                "log":   list(message_log),
            },
        }
    try:
        conn.sendall((json.dumps(snapshot) + "\n").encode())
        # Mantém a conexão aberta (monitor só lê)
        while True:
            if not conn.recv(1):
                break
    except OSError:
        pass
    finally:
        with lock:
            if conn in monitor_conns:
                monitor_conns.remove(conn)
        conn.close()


def heartbeat_checker():
    """Marca workers como offline se não enviarem nada por >5s."""
    while True:
        time.sleep(3)
        agora = datetime.now()
        with lock:
            for wid, s in process_stats.items():
                try:
                    last = datetime.strptime(s["last_seen"], "%H:%M:%S").replace(
                        year=agora.year, month=agora.month, day=agora.day
                    )
                    delta = (agora - last).total_seconds()
                    if delta > 5 and s["status"] == "🟢 online":
                        s["status"] = "🟡 idle"
                    elif delta > 15 and s["status"] != "🔴 offline":
                        s["status"] = "🔴 offline"
                except ValueError:
                    pass
        broadcast_to_monitors({"event": "stats", "data": dict(process_stats)})


def serve(port: int, handler):
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((HOST, port))
    srv.listen(16)
    print(f"[broker] escutando em {HOST}:{port}")
    while True:
        conn, addr = srv.accept()
        threading.Thread(target=handler, args=(conn, addr) if handler is handle_worker else (conn,),
                         daemon=True).start()


if __name__ == "__main__":
    threading.Thread(target=heartbeat_checker, daemon=True).start()
    threading.Thread(target=serve, args=(PORT_WORKERS, handle_worker), daemon=True).start()
    serve(PORT_MONITOR, handle_monitor)
