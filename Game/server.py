import socket
import threading
from player import Player
import pickle

server = "127.1.0.0"
port = 5555

# Creating a socket instance
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind to the specified IP and port
try:
    s.bind((server, port))
except socket.error as e:
    str(e)

# Listening to incoming connections
s.listen(2)
print("Waiting for a connection...")

players = [
    Player(350, 350, 50, 50, (255, 0, 0)),
    Player(100, 100, 50, 50, (0, 0, 255))
]


def threaded_client(conn, player):
    # Sends the player's details
    conn.send(pickle.dumps(players[player]))
    while True:
        try:
            # Receives updated position of this player
            data = pickle.loads(conn.recv(2048))
            players[player] = data

            if not data:
                print("Disconnected")
                break
            # Sends other player's details
            else:
                if player == 1:
                    reply = players[0]
                else:
                    reply = players[1]

            conn.sendall(pickle.dumps(reply))

        except:
            break

    print("Lost Connection")
    conn.close()


currentPlayer = 0
threads = []

while currentPlayer < 2:
    conn, addr = s.accept()
    print("Connected to:", addr)

    # Connect a new player by starting a new thread
    thread = threading.Thread(target=threaded_client,
                              args=(conn, currentPlayer))
    thread.start()
    threads.append(thread)
    currentPlayer += 1

for thread in threads:
    thread.join()
s.close()
print("Server Closed")