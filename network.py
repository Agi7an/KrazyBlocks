import socket
import pickle


class Network:

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "127.1.0.0"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    # Return the player
    def getPlayer(self):
        return self.p

    # Connect to the server => Creates a new player
    def connect(self):
        try:
            self.client.connect(self.addr)
            # Returns the player's details
            return pickle.loads(self.client.recv(2048))
        except:
            pass

    # Send the player's details to the server
    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            enemyPos = []
            for i in range(4):
                enemyPos.append(pickle.loads(self.client.recv(2048)))
            # print("Enemy Positions:", enemyPos)
            return enemyPos
        except socket.error as e:
            print(e)