import socket
import random

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432  # The port used by the server

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (HOST, PORT)
sock.connect(server_address)

transaction_menu = {"Transfer:1", "Balance:2"}

while True:
    print(transaction_menu)
    user_command = int(input("Your selection: "))
    if user_command == 1:
        receiver_id = input("Receiver id:")
        transfer_amount = input("Transfer amount:")
        query_string = "1 " + receiver_id + " " + transfer_amount
        #client_ui.send(query_string)
        request = bytes(query_string, 'utf-8')
        sock.sendall(request)
        response = sock.recv(1024)
        print(response)
        if int(response[0]) == '0':
            print("INCORRECT")
        else:
            print("SUCCESS")

    elif user_command == 2:
        query_string = str(2)
        #client_ui.send(query_string)
        request = bytes(query_string, 'utf-8')
        sock.sendall(request)
        #response = client_ui.recv()
        #print(response)

    else:
        print("Invalid command, Please try again")
        continue


data = sock.recv(1024)
print('Received', repr(data))
sock.close()





