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

def handle_msg(msg : Msg, server : socket.socket):
    log(msg)
    if(msg.type == MSG_NEW_PLAYER):
        name = msg.content
        if name not in players_name:
            clients_addr.append(msg.sender)
            players_name.append(name)
            respond = pickle.dumps(Msg(MSG_NEW_PLAYER, 'OK', (SERVER_IP, SERVER_PORT)))
            log('Respond', respond)
            server.sendto(respond, msg.sender)
        else:
            respond = pickle.dumps(Msg(MSG_NEW_PLAYER, 'FAIL', (SERVER_IP, SERVER_PORT)))
            log('Respond', respond)
            server.sendto(respond, msg.sender)
    elif(msg.type == MSG_MOVE_PAWN):
        data = pickle.dumps(msg, protocol=5)
        for addr in clients_addr:
            log('Respond', respond)
            server.sendto(data, addr)



def main():
    global quit
    client_connection = create_server_socket()
    
    listener = threading.Thread(target=receive_msgs_into_queue, args=[client_connection])
    listener.start()
    while not quit:
<<<<<<< HEAD
        try:
            msg = get_next_msg()
            if msg:
                handle_msg(msg, client_connection)
        except KeyboardInterrupt:
            log('Keyboard interupt')
            quit = True
        except Exception as ex:
            log(ex)
    listener.join(0)
    client_connection.close()
=======
        msg, client = server.recvfrom(1024)
        msg = pickle.loads(msg)
        handle_msg(msg, client, server)

>>>>>>> parent of d96e0d0 (Small refactoring)

if __name__ == '__main__':
    main()