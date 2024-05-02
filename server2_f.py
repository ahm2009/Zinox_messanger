import socket
import threading
import time
host = '127.0.0.1' # localhost
port = 55555
server =socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.bind((host, port))
server.listen()
clients=[]
nicknames =[]
check=False
list_message=[]

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:

        try:
            message = client.recv(1024)
            list_message = message.decode('utf-8').split('/')

            if list_message[1]=='message':
                with open('log.txt', 'a' , encoding='utf-8')as file:
                    file.write(message.decode('utf-8') + '\n')
            else:
                broadcast(message)         
        except IndexError: 
            broadcast(message)
        except UnicodeDecodeError:
            broadcast(message)
        except ConnectionResetError:
            index = clients.index(client)
            clients.remove(client)
            nickname = nicknames[index]
            nicknames.remove(nickname)
            broadcast(f'{nickname} left the group'.encode('utf-8'))
            broadcast('..'.encode('utf-8'))
            break



def receive():
    while True:
        client, address = server.accept()
        print(f'connected with {str(address)}')

        # client.send('NICK'.encode('utf-8'))
        nickname=client.recv(1024).decode('utf-8')
        time.sleep(0.05)
        client.send('log.txt'.encode('utf-8'))
        time.sleep(0.1)
        with open('log.txt', "rb") as file:
        # Read the file content
            file_data = file.read()

        client.send(str(len(file_data)).encode('utf-8'))
        time.sleep(0.1)

    # Send the file content to the client
        client.send(file_data)
        time.sleep(0.1)
        broadcast(f'{nickname} joined the chat!'.encode('utf-8'))
        broadcast('..'.encode('utf-8'))

        nicknames.append(nickname)
        clients.append(client)

        print(f'NICKname of the client is {nickname}!')
        # broadcast(f'{nickname} joined the chat!'.encode('utf-8'))
        # client.send("Connected to the server!".encode('utf-8'))


        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
print('server is listening...')
receive()
