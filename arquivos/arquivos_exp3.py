import os

# Criar pasta
os.mkdir("teste_diretorio")

# Verificar se existe e remover
if os.path.exists("teste_diretorio"):
    print("Diretorio existe")
    os.rmdir("teste_diretorio")
    print("Diretório removido.")