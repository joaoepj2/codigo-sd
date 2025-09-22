from multiprocessing import Process
import time

def tarefa(nome):
    for i in range(3):
        print(f"[{nome}] Passo {i}")
        # coloca o processo para dormir 1s
        time.sleep(1)

if __name__ == "__main__":
    p1 = Process(target=tarefa, args=("P1",))
    p2 = Process(target=tarefa, args=("P2",))
    
    p1.start()
    p2.start()
    
    p1.join()
    p2.join()
