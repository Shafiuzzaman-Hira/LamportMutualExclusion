#!/usr/bin/env python3

import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))

while True:
    sock.listen()
    conn, address = sock.accept()
    print('Connected by', address)
    try:
        request = conn.recv(1024)
        response = "$10" + str(request)
        res = bytes(response, 'utf-8')
        conn.sendall(res)

    finally:
        conn.close()
