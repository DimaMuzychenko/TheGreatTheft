import socket
import threading
import time
from traceback import print_tb



quit = False


def receving(sock : socket):
    global quit
    while not quit:
        try:
            data = sock.recv(1024)
            if data:
                print(data.decode('utf-8'))
        except Exception as ex:
            print(ex)
            quit = True
        time.sleep(0.2)



server_address = input('Type server address:\n')
server_address = server_address.split(':')

print('STARTING...')
connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP = server_address[0]
PORT = int(server_address[1])
connection.connect((IP, PORT))

th = threading.Thread(target=receving, args={connection})
th.start()

while not quit:
    try:
        msg = input()
        if msg != '':
            connection.send(msg.encode('utf-8'))
    except KeyboardInterrupt:
        quit = True
    except Exception as ex:
        print(ex)
        quit = True


th.join()
connection.close()