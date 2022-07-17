from ast import arg
import threading
from queue import Empty, Queue
from time import sleep
import pyperclip as pc
import socket
from dotenv import load_dotenv
from os import getenv
from json import loads

# all devices should be running this file in order to use same clipboard

load_dotenv()
server_port = int(getenv('server_port'))
server_ip = getenv('server_ip')
buffer_size = int(getenv('buffer_size'))
sending_state = False
receiving_state = False
threads = []
reset = False

def connect(ip, port):
    so = socket.socket()
    while True:
        try:
            so.connect((ip, port))
            print("Universal Keyboard Connected ::", check_connection(so))
            return so
        except:
            print("Connection Error..!!")
            sleep(3)

def check_connection(so):
    try:
        so.send("ping".encode())
        if(so.recv(50).decode().lower() == 'pong'):
            return True
        return False
    except:
        return False

def client_copy(so):
    while True:
        data_copied = pc.waitForNewPaste()
        if reset:
            break
        # print("Copied ::", data_copied)
        t = threading.Thread(target=send_socket_pack, args=(so, data_copied))
        threads.append(t)
        t.start()

def send_socket_pack(so, data_copied):
    while True:
        try:
            so.send(data_copied.encode())
            break
        except:
            print("Sending Connection Error..!!")
            sleep(3)
        if reset:
            break

def recv_socket_pack(so):
    while True:
        try:
            data = so.recv(buffer_size).decode()
            if data.strip() == '':
                so.close()
                break
            elif data[:4].lower() == "ping":
                send_socket_pack(so, "pong")
            else:
                pc.copy(data)
            # print("Received ::", data)
        except:
            print("Receiving Connection Error..!!")
            sleep(3)


while True:
    reset = False
    so = connect(server_ip, server_port)
    t1 = threading.Thread(target=client_copy, args=(so,))
    t1.start()
    recv_socket_pack(so)
    reset = True
    pc.copy('')
    t1.join()
    print("Restarting...")