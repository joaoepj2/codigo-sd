import socket
 
host = "52.90.82.178"
port = 50003


 
 
sock = socket.socket(socket.AF_INET, # Internet
    socket.SOCK_DGRAM) # UDP


for counter in range(1, 101):
    print("Enviando a mensagem " + str(counter) + " para o IP " + str(host) + ", porta " + str(port))
    message = "Eu sou o Datagrama numero " + str(counter)
    messageBytes = bytearray(message, "ascii")
    sock.sendto(messageBytes, (host, port))