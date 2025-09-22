import time
import psutil
import os

def memoria_usada():
    processo = psutil.Process(os.getpid())
    return processo.memory_info().rss / 1024**2

objetos = []

for i in range(20):
    objetos.append([0] * 100_000)  # Ocupa memória
    print(f"Passo {i+1}: Memória = {memoria_usada():.2f} MB")
    time.sleep(0.2)