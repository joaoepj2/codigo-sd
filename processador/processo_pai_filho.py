from multiprocessing import Process
import os


def mostrar_pid():
    print(f"Processo filho: PID = {os.getpid()}")

if __name__ == "__main__":
    print(f"Processo pai: PID = {os.getpid()}")
    # pede S.O. para criar processo filho
    p = Process(target=mostrar_pid)
    print("Processo filho criado") 
    p.start() # autoriza S.O. a rodar filho
    #print("Durante")
    #p.join() # pai espera pela morte do filho para continuar
    print("Processo filho morreu")

