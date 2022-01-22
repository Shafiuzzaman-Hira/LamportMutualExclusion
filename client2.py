from typing import Any

import constants
from lamport_mutex import *
from queue import PriorityQueue
import time

client_id = 2
ip = constants.HOST
port = constants.CLIENT2_PORT

local_clock: int = 0
q: PriorityQueue[Any] = PriorityQueue()
print_lock = threading.Lock()


# thread function
def threaded(c, ):
    global local_clock
    global q

    while True:
        data = c.recv(1024)  # data received from client
        data = data.decode()
        print("Request received..")
        if not data:
            print('Bye')
            print_lock.release()  # lock released on exit
            break

        print("Timestamp of sender: " + str(data))

        print("Existing queue of client " + str(client_id) + ":")
        if len(q.queue) < 0:
            print("Empty")
        for i in range(len(q.queue)):
            print(q.queue[i])

        parameter_list = data.split(".")
        # print(parameter_list)
        if parameter_list[0] == 'RELEASE':
            q.get()
            data = "DONE"
        else:
            sender_clock = int(parameter_list[0])
            local_clock = max(sender_clock, local_clock) + 1
            print("Updated clock: " + str(local_clock) + "." + str(client_id))

            sender_id = int(parameter_list[1])
            q.put((local_clock, sender_id))
            data = str(local_clock) + "." + str(client_id)  # reply

        print("Updated queue of client " + str(client_id) + ":")
        for i in range(len(q.queue)):
            print(q.queue[i])

        # print("Client " + str(client_id)) + " replied"
        c.sendall(str(data).encode())

    # connection closed
    c.close()


def accepting_request(ip, port):
    global local_clock

    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s1.bind((ip, port))
    s1.listen()
    print("Accepting requests..")

    local_clock = local_clock + 1
    print("Local clock " + str(local_clock) + "." + str(client_id))

    while True:
        c, addr = s1.accept()
        # lock acquired by client
        print_lock.acquire()
        #print('Connected to :', addr[0], ':', addr[1])

        # Start a new thread and return its identifier
        start_new_thread(threaded, (c,))


def send_request(server_ip, peers):
    global local_clock
    global q
    print("Putting request in local queue")
    q.put((client_id, local_clock))
    no_of_replies = 0
    for peer in peers:
        local_clock = local_clock + 1
        message = str(local_clock) + "." + str(client_id)
        print("Local clock: " + message)

        print("Sending request to " + str(server_ip) + ":" + str(peer))
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((server_ip, peer))

        time.sleep(3)
        s.sendall(message.encode())
        response = s.recv(1024)
        decoded_response = response.decode()
        print("Received reply from client " + str(client_id) + " with timestamp " + str(decoded_response))
        if decoded_response is not None:
            no_of_replies = no_of_replies + 1
        print("No of replies: " + str(no_of_replies))
        if no_of_replies == constants.NO_OF_CLIENTS - 1 & q.queue[0] > (client_id, local_clock):
            print("Permission Grated")
            return 1
        s.close()


def release(server_ip, peers):
    print("Remove from own queue")
    while not q.empty():
        q.get()

    for peer in peers:
        message = "RELEASE,"
        print("Sending release request to " + str(server_ip) + ":" + str(peer))
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((server_ip, peer))
        s.sendall(message.encode())
        response = s.recv(1024)
        decoded_response = response.decode()
        if decoded_response == "DONE":
            print("Queue update of client " + str(client_id))

        if decoded_response is not None:
            no_of_replies = no_of_replies + 1
        print("No of replies: " + str(no_of_replies))
        print(q.queue[0])
        print((client_id, local_clock))
        if no_of_replies == constants.NO_OF_CLIENTS - 1 & q.queue[0] > (client_id, local_clock):
            print("Request released successfully")
            return 1
        s.close()


def main():
    print("Client " + str(client_id) + " is in the network")
    print("Address " + str(ip) + ":" + str(port))
    accepting_request(ip, port)


if __name__ == "__main__":
    main()
