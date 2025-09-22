import os

# CWD - Current Working Directory 
# Caminho atual
caminho = os.getcwd()
print(f"Diretório atual: {caminho}")

# Listar conteúdo
conteudo = os.listdir(caminho)
print("Conteúdo do diretório:")
for item in conteudo:
    print(" -", item)
