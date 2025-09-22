import psutil
import os
import time

def memoria_loop():
    proc = psutil.Process(os.getpid())
    for i in range(50):
        print(f"Uso de memória: {proc.memory_info().rss / 1024**2:.2f} MB")
        time.sleep(1)

memoria_loop()