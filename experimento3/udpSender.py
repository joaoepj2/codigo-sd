import socket
 
host = "44.201.233.10"
port = 50000


 
 
sock = socket.socket(socket.AF_INET, # Internet
    socket.SOCK_DGRAM) # UDP


for counter in range(1, 1000):
    print("Enviando a mensagem " + str(counter) + " para o IP " + str(host) + ", porta " + str(port))
    message = "Eu sou o Datagrama numero " + str(counter)
    messageBytes = bytearray(message, "ascii")
    sock.sendto(messageBytes, (host, port))