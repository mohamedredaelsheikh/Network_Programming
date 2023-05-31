import socket
import pickle

# The Network class is used for client-server communication using sockets.
class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # It connects to a server at the specified address and port.
        self.server = "127.0.0.1"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.player = self.connect()
    # The `getPlayer` method returns the player received from the server.
    def getPlayer(self):
        return self.player
    
    # The `connect` method attempts to establish a connection with the server.
    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass
    # The `send` method sends data to the server and receives a response.
    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(2048*2))
        except socket.error as e:
            print(e)



