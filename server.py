import socket
import threading
from player import Player
import pickle
import signal

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
    Player(0, 0, 50, 50, (255, 0, 0)),
    Player(100, 100, 50, 50, (0, 0, 255)),
    Player(100, 0, 50, 50, (0, 255, 0)),
    Player(0, 100, 50, 50, (255, 255, 0)),
    Player(200, 200, 50, 50, (255, 0, 255))
]

currentPlayer = 0
threads = []


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
                for i in range(5):
                    if i != player:
                        reply = players[i]
                        print(i, reply)
                        conn.sendall(pickle.dumps(reply))
                print("\n")

        except:
            break

    print("Lost Connection")
    conn.close()


while currentPlayer < 5:
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