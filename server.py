import socket
import threading
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print("socket created")
s.bind(('localhost',9998))
print("waiting for connections")
s.listen()
clients = []
nicknames = []

def broadcast(message):
    for client in clients:
         client.send(message)
   
    

def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)
            broadcast(message)
        except:
            #Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break


def receive():
    while True:
        try:
            # Accept Connection
            client, address = s.accept()
            print("Connected with {}".format(str(address)))

            # Request And Store Nickname
            client.send('NICK'.encode('ascii'))
            nickname = client.recv(1024).decode('ascii')
            nicknames.append(nickname)
            clients.append(client)

            # Print And Broadcast Nickname
            print("Nickname is {}".format(nickname))
            broadcast("{} joined!".format(nickname).encode('ascii'))
            client.send('Connected to server!'.encode('ascii'))

            # Start Handling Thread For Client
            thread = threading.Thread(target=handle, args=(client,))
            thread.start()
        except:
            break
receive()