import socket
import select
import time

host = "52.90.82.178"
port = 50004


 
 
sock = socket.socket(socket.AF_INET, # Internet
    socket.SOCK_DGRAM) # UDP


for counter in range(1, 101):
    #print("Enviando a mensagem " + str(counter) + " para o IP " + str(host) + ", porta " + str(port))
    message = "Eu sou o Datagrama numero " + str(counter)
    messageBytes = bytearray(message, "ascii")
    # Esse experimento envia uma sequencia de 100 mensagens
    # mas com um intervalo de tempo aleatório entre os envios
    time.sleep(0.2)
    sock.sendto(messageBytes, (host, port))

sock.sendto(b'fim', (host, port))

# Wait for a packet for 5 seconds
ready = select.select([sock], [], [], 5)
if ready:
    serverData, addr = sock.recvfrom(51200)
    print(serverData.decode())

sock.close()