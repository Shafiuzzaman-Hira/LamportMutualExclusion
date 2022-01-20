import constants
from lamport_mutex import *

client_id = 3
local_clock = 0.3
queue = []
print_lock = threading.Lock()
ip = constants.HOST
port = constants.CLIENT3_PORT

# thread function
def threaded(c, ):
    global local_clock
    global queue

    while True:
        # data received from client
        data = c.recv(1024)
        data = data.decode()
        if not data:
            print('Bye')

            # lock released on exit
            print_lock.release()
            break

        parameter_list = data.split(",")
        print(parameter_list)
        msg_timestamp = float(parameter_list[1])
        print("Timestamp of sender" + str(msg_timestamp))
        local_clock = max(msg_timestamp, local_clock) + 1
        print("Updated clock " + str(local_clock))

        sender_id = float(parameter_list[1])
        queue.append((sender_id, local_clock))
        print("queue of client " + str(client_id))
        print(queue)
        data = 1  #reply
        print("Reply from client" + str(client_id))
        c.sendall(str(data).encode())

    # connection closed
    c.close()


def accepting_request(ip, port):
    global local_clock
    local_clock = local_clock + 1
    print("Local clock" + str(local_clock))
    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s1.bind((ip, port))
    s1.listen()
    print("Accepting requests..")
    while True:
        c, addr = s1.accept()
        # lock acquired by client
        print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])

        # Start a new thread and return its identifier
        start_new_thread(threaded, (c,))

    s1.close()


def client3_request(server_ip, peers):
    global local_clock
    global queue
    print("Putting request in local queue")
    queue.append((client_id, local_clock))
    no_of_replies = 0
    for peer in peers:
        print("Sending request to " + str(server_ip) + ":" + str(peer))
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((server_ip, peer))
        local_clock = local_clock + 1
        message = str(client_id) + "," + str(local_clock)
        print(message)
        s.sendall(message.encode())
        response = s.recv(1024)
        decoded_response = response.decode()
        print("Reply: " + str(decoded_response))
        if int(decoded_response) == 1:
            no_of_replies = no_of_replies + 1
        print("No of replies: " + str(no_of_replies))
        if no_of_replies == constants.NO_OF_CLIENTS -1:
            print("Permission Grated")
            return 1
        s.close()


def main():
    print("Client " + str(client_id) + " is in the network")
    print("Address " + str(ip) + ":" + str(port))
    accepting_request(ip, port)


if __name__ == "__main__":
    main()
