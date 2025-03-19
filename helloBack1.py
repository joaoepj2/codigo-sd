import socket

host = "127.0.0.1"
port = 4000

server = socket.socket()
server.bind((host, port))
server.listen()
print(" Back1 Server listening on 4000...\n")
conn, addr = server.accept()
conn.send(b"Back1 Here!")
conn.close()