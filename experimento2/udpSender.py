import socket
 
UDP_IP = "44.201.233.10"
UDP_PORT = 5000
MESSAGE = b'Eu sou o Datagrama numero'

 
print("UDP target IP: %s" % UDP_IP)
print("UDP target port: %s" % UDP_PORT)
print("message: %s" % MESSAGE.decode()) # decode() converts bytearray to string
 
sock = socket.socket(socket.AF_INET, # Internet
    socket.SOCK_DGRAM) # UDP

#while True:
#MESSAGE = counter.to_bytes(1)
#counter = counter + 1

#for counter = 1
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))