import socket
 
UDP_IP = "0.0.0.0"
UDP_PORT = 50000
clientResponse = ""

sock = socket.socket(socket.AF_INET, # Internet
                      socket.SOCK_DGRAM) # UDP

sock.bind((UDP_IP, UDP_PORT))


print("udpReceiver aguardando a chegada de datagramas no IP "
       + socket.gethostbyname(socket.gethostname())
       + ", porta " + str(UDP_PORT))



while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    consoleMessage = "A message was received from " + str(addr)
    print(consoleMessage)
    sock.send(bytearray(consoleMessage))


