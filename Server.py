import socket
import pickle
import threading
from typing import *
from Packages.network import *
from Packages.Pawn import Pawn


    
clients_addr : List[Tuple[str, int]] = []
players_name : List[str] = []
pawns : List[Pawn] = []
quit = False

def handle_msg(msg : Msg, sender : Tuple[str, int], server : socket.socket):
    log(msg, 'Sender', sender)
    if(msg.type == MSG_NEW_PLAYER):
        name = msg.content
        if name not in players_name:
            clients_addr.append(sender)
            players_name.append(name)
            respond = pickle.dumps(Msg(MSG_NEW_PLAYER, 'OK'))
            log('Respond', respond, 'to', sender)
            server.sendto(respond, sender)
        else:
            respond = pickle.dumps(Msg(MSG_NEW_PLAYER, 'FAIL'))
            log('Respond', respond, 'to', sender)
            server.sendto(respond, sender)
    elif(msg.type == MSG_MOVE_PAWN):
        data = pickle.dumps(msg, protocol=5)
        for addr in clients_addr:
            log('Respond', respond, 'to', sender)
            server.sendto(data, addr)



def main():
    global quit
    client_connection = create_server()
    
    listener = threading.Thread(target=receive_msgs_into_queue, args=[client_connection])
    listener.run()
    while not quit:
        try:
            msg, sender = get_next_msg()
            if msg:
                handle_msg(msg, sender, client_connection)
        except KeyboardInterrupt:
            log('Keyboard interupt')
            quit = True
        except Exception as ex:
            log(ex)
    listener.join(0)
    client_connection.close()

if __name__ == '__main__':
    main()