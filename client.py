import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432  # The port used by the server

transaction_menu = {"Transfer:1", "Balance:2"}

while True:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (HOST, PORT)
    sock.connect(server_address)
    print(transaction_menu)
    user_command = int(input("Your selection: "))

    if user_command == 1:
        receiver_id = input("Receiver id:")
        transfer_amount = input("Transfer amount:")

        request = "1," + receiver_id + "," + transfer_amount
        stripped_request = request.strip()

        sock.sendall(stripped_request.encode())
        response = sock.recv(1024)
        decoded_response = response.decode()
        print(decoded_response)

        if int(response[0]) == '0':
            print("INCORRECT")
        else:
            print("SUCCESS")

    elif user_command == 2:
        request = str(2)
        sock.sendall(request.encode())
        response = sock.recv(1024)
        print("Balance: " + response.decode())

    else:
        print("Invalid command, Please try again")
        continue

    sock.close()
