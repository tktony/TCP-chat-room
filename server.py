import threading
import socket

# 1. Define a Host address and a port for our server
host = '127.0.0.1' # localhost
port = 55555       # don't take reserved, well known ports (e.g.80, 1-10000)

# 2. Start the service 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 3. Bind the server into the host and IP Address (server is bound to the localhoast on port 55555)
server.bind((host, port)) 

# 4. Put the server in listening mode for new connections
server.listen()

clients = []
nicknames = []

# broadcast function - sends a message to all the connected clients 
def broadcast(message):
    for client in clients:
        client.send(message)

# handle function - handles the connection
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            client.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat!'.encode('ascii'))
            nicknames.remove(nickname)
            break

# receiver function
def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of the client is {nickname}!')
        broadcast(f'{nickname} joined the chat!'.encode('ascii'))
        client.send('Connected to the server!'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print('Server is listening...')
receive()

