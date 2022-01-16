import socket
import random

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_id = random.randint(10001,99999)
client_address = (HOST, PORT)
request = str(client_id)
sock.connect(client_address)
request= bytes(request, 'utf-8')
sock.sendall(request)

data = sock.recv(1024)

print('Received', repr(data))