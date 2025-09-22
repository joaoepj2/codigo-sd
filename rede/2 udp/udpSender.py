import socket
 
host = "52.90.82.178"
port = 50002
message = b'Eu sou um Datagrama!'

 
 
sock = socket.socket(socket.AF_INET, # Internet
    socket.SOCK_DGRAM) # UDP


print("Enviando uma mensagem para o IP " + str(host) + ", porta " + str(port))
sock.sendto(message, (host, port))
data, addr = sock.recvfrom(1024)
print("\nServer log: " + data.decode())