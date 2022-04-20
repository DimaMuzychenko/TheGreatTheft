import socket
import pickle
from typing import *
from Packages.network import *
from Packages.Pawn import Pawn


    
clients_addr : List[Tuple[str, int]] = []
players_name : List[str] = []
pawns : List[Pawn] = []
quit = False

def handle_msg(msg : Msg, sender : Tuple[str, int], server : socket.socket):
    if(msg.type == MSG_NEW_PLAYER):
        name = msg.content
        if name not in players_name:
            clients_addr.append(sender)
            players_name.append(name)
            respond = pickle.dumps(Msg(MSG_NEW_PLAYER, 'OK'))
            server.sendto(respond, sender)
        else:
            respond = pickle.dumps(Msg(MSG_NEW_PLAYER, 'FAIL'))
            server.sendto(respond, sender)
    elif(msg.type == MSG_MOVE_PAWN):
        data = pickle.dumps(msg, protocol=5)
        for addr in clients_addr:
            server.sendto(data, addr)





def main():
    server = create_server()
    while not quit:
        msg, client = server.recvfrom(1024)
        msg = pickle.loads(msg)
        handle_msg(msg, client, server)


if __name__ == '__main__':
    main()