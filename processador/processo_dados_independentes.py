from multiprocessing import Process

x = 0

def mudar_x():
    global x
    x = 42
    print("Filho: x =", x)

if __name__ == "__main__":
    print("Pai antes: x =", x)
    p = Process(target=mudar_x)
    p.start()
    p.join()
    print("Pai depois: x =", x)
