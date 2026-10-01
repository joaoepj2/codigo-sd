"""
ipc_memoria.py — Processos se comunicando via memória compartilhada.

Parte 1: multiprocessing.Value / Array  (alto nível, com lock embutido)
Parte 2: multiprocessing.shared_memory  (bytes brutos, você define o formato)

Funciona em Linux, macOS e Windows (por isso o `if __name__ == "__main__"`).
"""

import struct
import time
from multiprocessing import Process, Value, Array, Lock
from multiprocessing import shared_memory


# ════════════════════════════════════════════════════════════════
#  Parte 1 — Value e Array
# ════════════════════════════════════════════════════════════════

def incrementa(contador, vezes):
    for _ in range(vezes):
        with contador.get_lock():      # sem o lock, haveria condição de corrida
            contador.value += 1


def preenche(vetor, inicio, fim, fator):
    for i in range(inicio, fim):
        vetor[i] = i * fator


def parte1():
    print("── Parte 1: Value e Array ──")

    contador = Value("i", 0)           # 'i' = int; já vem com um lock interno
    vetor = Array("i", 10)             # 10 inteiros, todos zero

    # 4 processos incrementam o MESMO contador
    procs = [Process(target=incrementa, args=(contador, 10_000)) for _ in range(4)]
    for p in procs: p.start()
    for p in procs: p.join()
    print(f"contador final: {contador.value}  (esperado: 40000)")

    # 2 processos preenchem metades diferentes do mesmo vetor
    p1 = Process(target=preenche, args=(vetor, 0, 5, 10))
    p2 = Process(target=preenche, args=(vetor, 5, 10, 100))
    p1.start(); p2.start(); p1.join(); p2.join()
    print(f"vetor: {list(vetor)}")


# ════════════════════════════════════════════════════════════════
#  Parte 2 — shared_memory (produtor/consumidor com bytes brutos)
# ════════════════════════════════════════════════════════════════
#
# Layout do bloco (8 bytes de cabeçalho + 64 de mensagem):
#   [0:4]  flag  (int32): 0 = vazio, 1 = mensagem pronta, 2 = encerrar
#   [4:8]  tamanho da mensagem (int32)
#   [8:72] texto UTF-8

TAM = 72


def produtor(nome, mensagens):
    shm = shared_memory.SharedMemory(name=nome)    # anexa ao bloco existente
    for msg in mensagens:
        dados = msg.encode("utf-8")[:64]
        while struct.unpack_from("i", shm.buf, 0)[0] != 0:   # espera esvaziar
            time.sleep(0.01)
        struct.pack_into("i", shm.buf, 4, len(dados))
        shm.buf[8:8 + len(dados)] = dados
        struct.pack_into("i", shm.buf, 0, 1)                 # publica por último
    while struct.unpack_from("i", shm.buf, 0)[0] != 0:
        time.sleep(0.01)
    struct.pack_into("i", shm.buf, 0, 2)                     # sinal de fim
    shm.close()


def consumidor(nome):
    shm = shared_memory.SharedMemory(name=nome)
    while True:
        flag = struct.unpack_from("i", shm.buf, 0)[0]
        if flag == 1:
            n = struct.unpack_from("i", shm.buf, 4)[0]
            texto = bytes(shm.buf[8:8 + n]).decode("utf-8")
            print(f"[consumidor] recebeu: {texto!r}")
            struct.pack_into("i", shm.buf, 0, 0)             # libera o slot
        elif flag == 2:
            break
        else:
            time.sleep(0.01)
    shm.close()


def parte2():
    print("\n── Parte 2: shared_memory ──")
    shm = shared_memory.SharedMemory(create=True, size=TAM)
    shm.buf[:TAM] = bytes(TAM)                               # zera o bloco

    msgs = ["olá do produtor", "segunda mensagem", "terceira e última"]
    pc = Process(target=consumidor, args=(shm.name,))
    pp = Process(target=produtor, args=(shm.name, msgs))
    pc.start(); pp.start()
    pp.join(); pc.join()

    shm.close()
    shm.unlink()          # libera o bloco no SO (só o criador faz isso)


if __name__ == "__main__":
    parte1()
    parte2()