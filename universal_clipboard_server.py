from ast import arg
from audioop import add
import threading
from queue import Empty, Queue
import pyperclip as pc
import socket
from time import sleep
from dotenv import load_dotenv
from os import getenv
from json import loads

# all devices should be running this file in order to use same clipboard

load_dotenv()
server_port = int(getenv('server_port'))
buffer_size = int(getenv('buffer_size'))

clients = []
client_threads = []

def connect(port):
    so = socket.socket()
    while True:
        try:
            so.bind(('', port))
            so.listen()
            return so
        except Exception as e:
            print("Port binding Error ::", e)
            sleep(3)

def check_connection(client):
    try:
        client.send("ping".encode())
        if(client.recv(50).decode().lower() == 'pong'):
            return True
        return False
    except:
        return False

def accept_client(so):
    while True:
        conn, addr = so.accept()
        clients.append(conn)
        t = threading.Thread(target=recv_socket_pack, args=(conn,))
        client_threads.append(t)
        t.start()

def send_socket_pack(conn, data):
    while True:
        try:
            conn.send(data.encode())
            break
        except:
            print("Sending Connection Error..!!")
            sleep(3)

def recv_socket_pack(conn):
    while True:
        try:
            data = conn.recv(buffer_size).decode()
            if data.strip() == '':
                conn.close()
                clients.remove(conn)
                break
            if data[:4].lower() == "ping":
                send_socket_pack(conn, "pong")
            else:
                # pc.copy(data)
                for c in filter(lambda x:x!=conn, clients):
                    send_socket_pack(c, data)
            # print("Received ::", data)
        except:
            print("Receiving Connection Error..!!")
            sleep(3)


so = connect(server_port)
accept_client(so)