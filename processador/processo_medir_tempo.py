from multiprocessing import Process
import time

def esperar():
    time.sleep(2)

if __name__ == "__main__":
    inicio = time.time()

    p1 = Process(target=esperar)
    p2 = Process(target=esperar)

    p1.start()
    p2.start()
    p1.join()
    p2.join()

    fim = time.time()
    print(f"Tempo com processos: {fim - inicio:.2f} segundos")
