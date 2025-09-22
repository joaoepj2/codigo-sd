import gc
import psutil
import os

def memoria_usada():
    processo = psutil.Process(os.getpid())
    mem = processo.memory_info().rss
    print(f"Memória usada: {mem / 1024**2:.2f} MB")

memoria_usada()
a = 0
memoria_usada()

del a  # Remove referência
gc.collect()  # Força coleta de lixo
memoria_usada()