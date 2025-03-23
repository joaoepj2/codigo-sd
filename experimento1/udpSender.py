import socket
 
UDP_IP = "127.0.0.1"
UDP_PORT = 50000
MESSAGE = b'Hello, World!'
 
 
sock = socket.socket(socket.AF_INET, # Internet
    socket.SOCK_DGRAM) # UDP

print("Enviando uma mensagem para o IP %s, Porta %d" % (UDP_IP,  UDP_PORT))
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))