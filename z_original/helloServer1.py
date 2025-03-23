import socket
host = "127.0.0.1"
port = 6789
server = socket.socket()
server.bind((host, port))
server.listen()
print(" Hello Server listening on 6789...\n")
conn, addr = server.accept()
conn.send(b"Hello Uniube!")
conn.close()