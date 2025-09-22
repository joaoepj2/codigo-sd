import os

# Criar um arquivo
with open("experimento.txt", "w") as f:
    f.write("Teste de sistema de arquivos.\n")

# Renomear
os.rename("experimento.txt", "renomeado.txt")

# Apagar
os.remove("renomeado.txt")
print("Arquivo criado, renomeado e removido com sucesso.")
