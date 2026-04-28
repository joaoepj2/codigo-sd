"""
workers.py — Simula múltiplos processos workers conectados ao broker.

Cada worker roda em uma thread separada e envia mensagens JSON
ao broker via socket TCP na porta :5555.

Uso:
    python workers.py
"""

import socket
import json
import time
import random
import threading

HOST = "127.0.0.1"
PORT = 5555

TAREFAS = [
    "processar_imagem", "enviar_email", "gerar_relatorio",
    "sincronizar_bd",   "comprimir_log", "verificar_saude",
    "atualizar_cache",  "exportar_csv",
]

ERROS = [
    "timeout ao conectar",
    "arquivo não encontrado",
    "memória insuficiente",
    "permissão negada",
]


def worker(wid: str, intervalo_base: float, role: str):
    """
    Conecta ao broker e fica enviando mensagens periodicamente.

    wid            — identificador único, ex: "worker-A"
    intervalo_base — segundos entre mensagens (com jitter)
    role           — "producer" ou "consumer"
    """
    while True:  # reconecta se cair
        try:
            with socket.create_connection((HOST, PORT)) as conn:
                print(f"[{wid}] conectado ao broker")
                while True:
                    # Chance de enviar erro
                    if random.random() < 0.25:
                        msg = {
                            "worker_id": wid,
                            "type":      "error",
                            "payload":   random.choice(ERROS),
                        }
                    else:
                        tarefa = random.choice(TAREFAS)
                        duracao = round(random.uniform(0.1, 2.5), 2)
                        msg = {
                            "worker_id": wid,
                            "type":      "task" if role == "producer" else "result",
                            "payload":   f"{tarefa} [{duracao}s]",
                        }

                    conn.sendall((json.dumps(msg) + "\n").encode())

                    # Intervalo com jitter aleatório
                    time.sleep(intervalo_base + random.uniform(0, intervalo_base))

        except (ConnectionRefusedError, OSError) as e:
            print(f"[{wid}] broker indisponível: {e} — tentando em 3s")
            time.sleep(3)


if __name__ == "__main__":
    configuracoes = [
        ("worker-A", 0.8,  "producer"),
        ("worker-B", 1.2,  "producer"),
        ("worker-C", 0.5,  "producer"),
        ("worker-D", 2.0,  "consumer"),
        ("worker-E", 1.5,  "consumer"),
    ]

    threads = []
    for wid, intervalo, role in configuracoes:
        t = threading.Thread(
            target=worker,
            args=(wid, intervalo, role),
            daemon=True,
        )
        t.start()
        threads.append(t)
        time.sleep(0.2)   # evita conexões simultâneas na subida

    print(f"[workers] {len(threads)} workers rodando — Ctrl+C para parar")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[workers] encerrando")
