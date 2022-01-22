import socket
import constants
from blockchain import *

HOST = constants.HOST
PORT = constants.BLOCKCHAIN_PORT
TRANSACTION_FAILED = 0
TRANSACTION_SUCCEED = 1
blockchain = Blockchain()
chain_data = []


def print_blockchain():
    print("Current Blockchain")
    for i in chain_data:
        print("sender: ", i.sender, " receiver: ", i.receiver, " amount: ", i.amount)




def check_balance(client_id):
    chain_data = get_chain(blockchain)
    balance = constants.INITIAL_BALANCE
    if chain_data[0] == 'genesis':
        return balance
    else:
        #print_blockchain()
        reversed_chain = chain_data
        reversed_chain.reverse()
        for block in reversed_chain:
            if block[0] == client_id:
                balance = balance - block[2]
            elif block[1] == client_id:
                balance = balance + block[2]
            else:
                continue
        return balance


def transfer_balance(sender, receiver, amount):
    global blockchain
    print(
        "Initiating transfer for sender {0}, received by: {1} and the amount is ${2}".format(str(sender), str(receiver),
                                                                                             str(amount)))
    sender_current_balance = check_balance(sender)
    print("Client" + str(sender) + " current balance: $" + str(sender_current_balance))
    receiver_current_balance = check_balance(receiver)
    print("Client" + str(receiver) + " current balance: $" + str(sender_current_balance))
    if sender_current_balance < amount:
        print("Transaction failed due to insufficient balance")
        return TRANSACTION_FAILED
    else:
        block_data = [sender, receiver, amount]
        #new_block = Blockchain_data(sender, receiver, amount)
        # current_block_data = []
        # previous_block = blockchain.print_previous_block()
        # previous_hash = blockchain.hash(previous_block)
        # block = blockchain.create_block(sender, receiver, amount, previous_hash)
        blockchain.add_block(block_data)
        sender_new_balance = sender_current_balance - amount
        receiver_new_balance = receiver_current_balance + amount
        print("Client" + str(sender) + " new balance: $" + str(sender_new_balance))
        print("Client" + str(receiver) + " new balance: $" + str(receiver_new_balance))
      #  blockchain = Blockchain()
        chain_data = get_chain(blockchain)
        print_blockchain()
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
        # print(decoded_request)
        request_list = decoded_request.split(",")
        print(request_list)
        sender = int((request_list[1]))
        print("Sender id: " + str(sender))

        if int(request_list[0]) == 2:
            balance = check_balance(sender)
            print(balance)
            conn.sendall(str(balance).encode())

        elif int(request_list[0]) == 1:
            receiver = int(request_list[2])
            amount = float(request_list[3])
            response = transfer_balance(sender, receiver, amount)
            # print(response)
            conn.sendall(str(response).encode())
    finally:
        conn.close()
