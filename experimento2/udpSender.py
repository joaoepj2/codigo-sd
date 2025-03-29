import socket
 
host = "44.201.233.10"
port = 50000
message = b'Eu sou um Datagrama!'

 
 
sock = socket.socket(socket.AF_INET, # Internet
    socket.SOCK_DGRAM) # UDP


print("Enviando uma mensagem para o IP " + str(host) + ", porta " + str(port))
sock.sendto(message, (host, port))
data, addr = sock.recvfrom(1024)
print("Mensagem: " + data.decode() + " foi recebida de ", addr)