import gc
import sys

class Ciclo:
    def __init__(self):
        self.ref = self

a = Ciclo()
print("Referências a 'a':", sys.getrefcount(a))  # Deve ser >1
del a
gc.collect()
print("Coletor de lixo rodou.")