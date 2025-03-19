import socket

host = "127.0.0.1"
port = 6789

client = socket.socket()
client.connect((host, port))
client.send(b"Knock knock!")
data = client.recv(1024)
print("From server: " + str(data.decode()))
client.close()