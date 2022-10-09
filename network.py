import socket
import pickle


class Network:
    def __init__(self):
        # here we initialize the client and server - you need your IPv4 in the server empty string
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "put server ip here"
        # put the same port - 5555 is which I use
        self.port = 5555
        self.address = (self.server, self.port)
        self.server_data = self.connect()

    def connect(self):
        # connecting the network to the server and sending the player initial information
        try:
            self.client.connect(self.address)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        # sending data from the client to the server
        try:
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(2048 * 20))
        except socket.error as e:
            print(e)

    def get_server_data(self):
        # getting the player initial data - player id - 0 or 1
        return self.server_data
