import socket
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--host", default="127.0.0.1", type=str)
parser.add_argument("--port", default=6789, type=int)
parser.add_argument("--message", default="Mensagem padrão!", type=str)
args = parser.parse_args()


client = socket.socket()
client.connect((args.host, args.port))
print("tcpClient sending message to ip %s, port %d ...\n" % (args.host, args.port))
client.send(bytearray(args.message, "utf-8"))
#data = client.recv(1024)
#print("From server: " + str(data.decode()))
client.close()