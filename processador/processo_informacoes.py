import psutil
import os

def info_processo():
    p = psutil.Process(os.getpid())
    print(f"PID: {p.pid}")
    print(f"Uso de memória: {p.memory_info().rss / 1024**2:.2f} MB")

info_processo()
