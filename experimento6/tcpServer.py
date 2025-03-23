import socket
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--host", default="127.0.0.1", type=str)
parser.add_argument("--port", default=6789, type=int)
args = parser.parse_args()


server = socket.socket()
server.bind((args.host, args.port))
server.listen()
print("tcpServer listening at ip %s, port %d ...\n" % (args.host, args.port))
conn, clientAddr = server.accept()
data = conn.recv(1024)
print(data.decode())

conn.close()