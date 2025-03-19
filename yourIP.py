import socket

hostname = socket.gethostname()
ipaddr = socket.gethostbyname(hostname)
print("Your IP is ", ipaddr)