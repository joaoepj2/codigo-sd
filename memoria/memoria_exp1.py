import psutil
import os

def memoria_usada():
    processo = psutil.Process(os.getpid())
    mem = processo.memory_info().rss  # Resident Set Size
    print(f"Memória usada: {mem / 1024**2:.2f} MB")

memoria_usada()
a = [0] * 10_000_000  # Aloca memória
memoria_usada()