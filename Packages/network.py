import pickle
import socket
import random
from .logging import log
from typing import *



DGRAM_SIZE = 1024
SERVER_IP = '25.16.200.3'
SERVER_PORT = 2620
CLIENT_IP = ''
CLIENT_PORT = -1


MSG_NEW_PLAYER = 0
MSG_GIVE_CARDS = 1
MSG_GIVE_TURN = 2
MSG_MOVE_PAWN = 3



class Msg:
    def __init__(self, msg_type : int, obj : Any, sender : Tuple[str, int] | None):
        self.type = msg_type
        self.sender = sender
        self.content = obj


def get_opened_port() -> int:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for i in range(100):
        port = random.randint(50000, 60000)
        res = s.connect_ex(("127.0.0.1", port))
        if res == 0:
            s.close()
            return port
    return -1
    

def create_client_socket() -> socket.socket:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    CLIENT_IP = socket.gethostbyname(socket.gethostname())
    CLIENT_PORT = get_opened_port()
    sock.bind((CLIENT_IP, CLIENT_PORT))    
    log("New socket", (CLIENT_IP, CLIENT_PORT), "is created")
    return sock


def create_server_socket() -> socket.socket:    
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((SERVER_IP, SERVER_PORT))
        log("New server", (SERVER_IP, SERVER_PORT), "is created")
    except socket.error as ex:
        log(ex)
    return server


def receive_msg(connection : socket.socket) -> Msg | None:
    data = None
    try:
        data = connection.recv(DGRAM_SIZE)
        data = pickle.loads(data)
    except socket.error as ex:
        log(ex)
    if type(data) == Msg:
        return data
    return None
 
msg_queue : List[Msg] = []
 
def receive_msgs_into(msg_queue, connection : socket.socket):
    while True:
        msg_queue.append(receive_msg(connection))
        

def receive_msgs_into_queue(connection : socket.socket):
    global msg_queue
    while True:
        msg_queue.append(receive_msg(connection))


def get_next_msg():
    try:
        return msg_queue.pop(0)
    except IndexError:
        return None

def pick_next_msg():
    try:
        return msg_queue[0]
    except IndexError:
        return None