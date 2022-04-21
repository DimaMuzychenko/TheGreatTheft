import socket

quit = False
clients = []

print('START...')
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#IP = socket.gethostbyname(socket.gethostname())
IP = '25.16.200.3'
PORT = 2620
server.bind((IP, PORT))
print('HOST', IP+':'+str(PORT))
server.setblocking(True)
print('WAITING FOR CONNECIONS...')

while not quit:
    try:
        data, addr = server.recvfrom(1024)
        if data:
            if addr not in clients:
                clients.append(addr)
                print('GOT NEW CONNECTION WITH', addr)
            for client in clients:
                if addr != client:
                    server.sendto(data, client)
    except KeyboardInterrupt:
        quit = True
        break
    except Exception as ex:
        with open('log.txt', 'a', encoding='utf-8') as file:
            file.write(ex)

server.close()
