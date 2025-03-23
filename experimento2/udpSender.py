import socket
 
host = "44.201.233.10"
port = 50000
message = b'Eu sou o Datagrama numero'

 
 
sock = socket.socket(socket.AF_INET, # Internet
    socket.SOCK_DGRAM) # UDP

# .decode() converts bytearray to string
#while True:
#MESSAGE = counter.to_bytes(1)
#counter = counter + 1

#for counter = 1
print("Enviando uma mensagem para o IP " + str(host) + ", porta " + str(port))
sock.sendto(message, (host, port))