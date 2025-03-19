import socket

host = "127.0.0.1"
port = 6789

back1Host = "127.0.0.1"
back1Port = 4000

back2Host = "127.0.0.1"
back2Port = 5000

server = socket.socket()
server.bind((host, port))
server.listen()
print(" Hello Front listening on 6789...\n")
conn, addr = server.accept()

client = socket.socket()
client.connect((back1Host, back1Port))
client.send(b"Hello Back 1")
back1Data = client.recv(1024)

client = socket.socket()
client.connect((back2Host, back2Port))
client.send(b"Hello Back 2")
back2Data = client.recv(1024)

client.close()


conn.send(back1Data + b" " + back2Data)
conn.close()