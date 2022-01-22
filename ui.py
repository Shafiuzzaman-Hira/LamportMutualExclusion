import constants
from client1 import send_request as client1_request
from client2 import send_request as client2_request
from client3 import send_request as client3_request
from client1 import release as client1_release
from client2 import release as client2_release
from client3 import release as client3_release
import socket

transaction_menu = {"Transfer: 1", "Balance: 2"}
blockchain_ip = constants.HOST
blockchain_port = constants.BLOCKCHAIN_PORT


def add_transaction(sender_id):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (blockchain_ip, blockchain_port)
    sock.connect(server_address)
    print(transaction_menu)
    user_command = int(input("Your selection: "))

    if user_command == 1:
        print("Sender id: " + str(sender_id))
        receiver_id = input("Receiver id:")
        transfer_amount = input("Transfer amount: $")

        request = "1," + str(sender_id) + "," + str(receiver_id) + "," + str(transfer_amount)
        stripped_request = request.strip()

        sock.sendall(stripped_request.encode())

        response = sock.recv(1024)
        decoded_response = response.decode()
        #print(decoded_response)

        if int(decoded_response) == 1:
            print("SUCCESS")
        else:
            print("INCORRECT")

    elif user_command == 2:
        print("Sender id: " + str(sender_id))
        request = "2," + str(sender_id)
        sock.sendall(request.encode())
        response = sock.recv(1024)
        print("Balance: " + response.decode())

    else:
        print("Invalid command, Please try again")
    sock.close()
    return


print("-----Client UI-----")
while True:
    client_id = int(input("Issue transaction from Client Id (1/2/3): "))
    if client_id == 1:
        port = constants.CLIENT1_PORT
        peer_clients = [constants.CLIENT2_PORT, constants.CLIENT3_PORT]
        print("Address:" + str(constants.HOST) + ":" + str(port))
        # print("Balance: $" + str(constants.INITIAL_BALANCE))
        granted_request = client1_request(constants.HOST, peer_clients)
        if granted_request == 1:
            print("Client " + str(client_id) + " is proceeding to blockchain")
            add_transaction(client_id)
        released_done = client1_release(constants.HOST, peer_clients)
        if released_done == 1:
            continue
    elif client_id == 2:
        port = constants.CLIENT2_PORT
        peer_clients = [constants.CLIENT1_PORT, constants.CLIENT3_PORT]
        print("Address:" + str(constants.HOST) + ":" + str(port))
        # print("Balance: $" + str(constants.INITIAL_BALANCE))
        granted_request = client2_request(constants.HOST, peer_clients)
        if granted_request == 1:
            print("Client " + str(client_id) + " is proceeding to blockchain")
            add_transaction(client_id)
        released_done = client2_release(constants.HOST, peer_clients)
        if released_done == 1:
            continue

    elif client_id == 3:
        port = constants.CLIENT3_PORT
        peer_clients = [constants.CLIENT1_PORT, constants.CLIENT2_PORT]
        print("Address:" + str(constants.HOST) + ":" + str(port))
        # print("Balance: $" + str(constants.INITIAL_BALANCE))
        granted_request = client3_request(constants.HOST, peer_clients)
        if granted_request == 1:
            print("Client " + str(client_id) + " is proceeding to blockchain")
            add_transaction(client_id)
        released_done = client3_release(constants.HOST, peer_clients)
        if released_done == 1:
            continue
    else:
        print("No such client")
