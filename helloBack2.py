import socket

host = "127.0.0.1"
port = 5000

server = socket.socket()
server.bind((host, port))
server.listen()
print(" Back2 Server listening on 5000...\n")
conn, addr = server.accept()
conn.send(b"Back2 Here!")
conn.close()