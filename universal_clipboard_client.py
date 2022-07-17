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
threads = []
reset = False
pinging = False

def connect(ip, port):
    while True:
        try:
            global reset
            so = socket.socket()
            so.connect((ip, port))
            reset = False
            return so
        except Exception as e:
            print("Connection Error..!!", e)
            sleep(3)

def check_connection(so):
    try:
        global reset 
        global pinging
        pinging = True
        print("checking connection")
        so.send("ping".encode())
    except:
        reset = True

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
        if reset:
            break
        else:
            sleep(3)

def recv_socket_pack(so):
    while True:
        try:
            global reset
            global pinging
            data = so.recv(buffer_size).decode()
            if data.strip() == '':
                so.close()
                reset = True
                break
            elif data[:4].lower() == "ping":
                send_socket_pack(so, "pong")
            elif pinging:
                if data[:4].lower() == "pong":
                    pinging = False
                    print("\t -> connected.")
                else:
                    reset = True
                    break
            else:
                pc.copy(data)
                
            # print("Received ::", data)
        except Exception as e:
            print("Receiving Connection Error..!!", e)
            if reset:
                break
            else:
                sleep(3)


while True:
    so = connect(server_ip, server_port)
    print("Universal Keyboard Connected..!!")
    t1 = threading.Thread(target=client_copy, args=(so,))
    t1.start()
    t2 = threading.Thread(target=recv_socket_pack, args=(so,))
    t2.start()
    while True:
        t3 = threading.Thread(target=check_connection, args=(so,))
        t3.start()
        t3.join()
        if reset:
            break
        else:
            sleep(10)
    # print("RESET var ::", reset)
    pc.copy('')
    t1.join()
    t2.join()
    print("Restarting...")