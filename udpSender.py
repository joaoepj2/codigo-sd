import socket
 
UDP_IP = "18.188.204.225"
UDP_PORT = 80
MESSAGE = b'Hello, World!'
counter = 0
 
print("UDP target IP: %s" % UDP_IP)
print("UDP target port: %s" % UDP_PORT)
print("message: %s" % MESSAGE.decode()) # decode() converts bytearray to string
 
sock = socket.socket(socket.AF_INET, # Internet
    socket.SOCK_DGRAM) # UDP

#while True:
#MESSAGE = counter.to_bytes(1)
#counter = counter + 1

sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))