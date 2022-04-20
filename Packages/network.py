import pickle
import socket
import random
from typing import *

from matplotlib.pyplot import connect
from config import SERVER_IP, SERVER_PORT, DGRAM_SIZE


DGRAM_SIZE = 1024
SERVER_IP = '25.16.200.3'
SERVER_PORT = 2620
SERVER_ADDRESS = (SERVER_IP, SERVER_PORT)

MSG_NEW_PLAYER = 0
MSG_GIVE_CARDS = 1
MSG_GIVE_TURN = 2
MSG_MOVE_PAWN = 3



class Msg:
    def __init__(self, msg_type : int, obj : Any):
        self.type = msg_type
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
    

def create_socket() -> socket.socket:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    IP = socket.gethostbyname(socket.gethostname())
    PORT = get_opened_port()
    sock.bind((IP, PORT))
    return sock


def create_server() -> socket.socket:    
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((SERVER_IP, SERVER_PORT))
    except socket.error as ex:
        with open('log.txt', 'w') as log_file:
            print(ex, file=log_file)
    return server


def receive_msg(connection : socket.socket) -> Msg | None:
    data = connection.recv(DGRAM_SIZE)
    data = pickle.loads(data)
    if data is Msg:
        return data
    return None
    