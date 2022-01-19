#!/usr/bin/env python3

import socket
from blockchain import Blockchain

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
TRANSACTION_FAILED = 0
TRANSACTION_SUCCEED = 1
blockchain = []


def check_balance(client_address):
    balance = 10  # starting balance $10 as stated in the specification
    for block in blockchain:
        if block.sender == client_address:
            balance = balance - block.amount
        elif block.receiver == client_address:
            balance = balance + block.amount
        else:
            continue
    return balance


def transfer_balance(sender, receiver, amount):
    print(
        "Initiating transfer for sender {0}, received by: {1} and the amount is ${2}".format(str(sender), str(receiver),
                                                                                             str(amount)))
    sender_current_balance = check_balance(sender)
    print(str(sender) + " current balance: $" + str(sender_current_balance))
    if sender_current_balance < amount:
        print("Transaction failed due to insufficient balance")
        return TRANSACTION_FAILED
    else:
        new_block = Blockchain(sender, receiver, amount)
        blockchain.append(new_block)
        sender_new_balance = sender_current_balance - amount
        print(blockchain)
        return TRANSACTION_SUCCEED


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((HOST, PORT))
print("Blockchain master started..")
while True:
    sock.listen()
    print("Waiting for connection..")
    conn, address = sock.accept()
    print('Connected by', address)
    try:
        request = conn.recv(1024)
        decoded_request = request.decode()
        print(decoded_request)
        request_list = decoded_request.split(",")
        print(request_list)
        sender = int((request_list[-1]))
        balance = check_balance(sender)
        print(balance)

        if int(request_list[0]) == 2:
            conn.sendall(str(balance).encode())

        elif int(request_list[0]) == 1:
            receiver = int(request_list[1])
            amount = float(request_list[2])
            response = transfer_balance(sender, receiver, amount)
            print(response)
            conn.sendall(str(response).encode())
    finally:
        conn.close()
