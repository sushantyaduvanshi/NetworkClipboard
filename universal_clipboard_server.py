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
        data_copied = conn.recv().decode()
        queue.put(data_copied)
        pc.copy(data_copied)
        conn.close()


q = Queue()
t1 = threading.Thread(target=server, args=(q,))
t1.start()