from pydoc import cli
import socket

quit = False
clients = []

print('START...')
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#IP = socket.gethostbyname(socket.gethostname())
IP = '25.16.200.3'
PORT = 2620
server.bind((IP, PORT))
print('HOST', IP+':'+str(PORT))
server.listen(2)
server.setblocking(True)
print('WAITING FOR CONNECIONS...')

while not quit:
    try:
        client, address = server.accept()
        server.setblocking(False)
    except socket.error:
        pass
    except KeyboardInterrupt:
        quit = True
        break
    if client not in clients:
        print('GOT NEW CONNECTION FROM', address[0]+':'+str(address[1]))
        clients.append(client)
        client.setblocking(0)
        client.send('You are connected'.encode('utf-8'))

    for client in clients:
        try:
            data = client.recv(1024)
            if data:
                for c in clients:
                    if client != c:
                        try:
                            c.send(data)
                        except:
                            clients.remove(c)
        except:
            pass

server.close()
