import threading
from queue import Empty, Queue
import pyperclip as pc
import socket
from dotenv import load_dotenv
from os import getenv
from json import loads

# all devices should be running this file in order to use same clipboard

load_dotenv()
port = int(getenv('port'))
other_ip = loads(getenv('other_ip'))

def server(queue):

    so = socket.socket()
    print("server socket created")
    
    so.bind(('', port))

    so.listen()

    while True:

        conn, addr = so.accept()
        data_copied = conn.recv(1024).decode()
        queue.put(data_copied)
        pc.copy(data_copied)
        conn.close()

def client(queue):

    while True:

        pc.waitForNewPaste()

        data_copied = pc.paste()

        if(queue.empty() or queue.get() != data_copied):

            for ip in other_ip:
                t = threading.Thread(target=send_socket_pack, args=(ip, port, data_copied))
                t.start()
        
        else:
            pass

def send_socket_pack(ip, port, data_copied):
    print(ip, port, "*****")
    print(data_copied, "*****")
    so = socket.socket()
            
    try:

        so.connect((ip, port))

        so.send(data_copied.encode())

    except (ConnectionRefusedError, TimeoutError):
        print("Connection Error..!!")

    finally:
        so.close()


q = Queue()
t1 = threading.Thread(target=server, args=(q,))
t2 = threading.Thread(target=client, args=(q,))
t1.start()
t2.start()