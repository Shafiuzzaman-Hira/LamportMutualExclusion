import constants
from client1 import client1_request
from client2 import client2_request
from client3 import client3_request


def show_ui():
    while True:
        print("-----Client UI-----")
        client_id = int(input("Issue transaction from Client Id (1/2/3): "))
        if client_id == 1:
            port = constants.CLIENT1_PORT
            peer_clients = [constants.CLIENT2_PORT, constants.CLIENT3_PORT]
            print("Address:" + str(constants.HOST) + ":" + str(port))
            # print("Balance: $" + str(constants.INITIAL_BALANCE))
            granted_request = client1_request(constants.HOST, peer_clients)
            if granted_request == 1:
                print("I am proceeding to blockchain")

        elif client_id == 2:
            port = constants.CLIENT2_PORT
            peer_clients = [constants.CLIENT1_PORT, constants.CLIENT3_PORT]
            print("Address:" + str(constants.HOST) + ":" + str(port))
            # print("Balance: $" + str(constants.INITIAL_BALANCE))
            granted_request = client2_request(constants.HOST, peer_clients)
            if granted_request == 1:
                print("I am proceeding to blockchain")
        elif client_id == 3:
            port = constants.CLIENT3_PORT
            peer_clients = [constants.CLIENT1_PORT, constants.CLIENT2_PORT]
            print("Address:" + str(constants.HOST) + ":" + str(port))
            # print("Balance: $" + str(constants.INITIAL_BALANCE))
            granted_request = client3_request(constants.HOST, peer_clients)
            if granted_request == 1:
                print("I am proceeding to blockchain")
        else:
            print("No such client")

show_ui()