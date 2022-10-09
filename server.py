import socket
import pickle
from _thread import *
from game import Game

# server - put your IPv4 in the empty string
server = "192.168.0.155"
# I am typically using port 5555 as it is most likely to be free
port = 5555

# initializing the socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# initializing the server
try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

# listening for connections - you can change the number to determine the max connections, it can be empty as well
s.listen(2)
print("[SERVER STARTED] - Waiting for a connection")

# setting the players variable to -1 so that when we have 2 players, they will be 0 and 1,
# and we can use their id's for accessing the lists from the Game Object
players = -1
game = None


# this is the thread for every player
def threaded_client(connection, player):
    global game, players

    # the first thing that we will send to the client will be the player id
    connection.send(str.encode(str(player)))
    reply = ""

    # here is the place where all the sending/receiving information and updating the players is happening
    while True:
        try:
            data = connection.recv(2048 * 5).decode()

            # if the game is already loaded
            if game is not None:
                # if data is empty, we break
                if not data:
                    break
                else:
                    # if data is not empty, we can give some commands which are sent from the clients
                    if data == "get":
                        reply = game

                    elif data == "connect":
                        game.connect_player(player)
                        reply = game

                    elif data == "square_update":
                        reply = game.get_squares(player)
                        game.squares_need_update[player] = False

                    elif data == "reset":
                        game.reset()
                        reply = game

                    elif data == "disconnect":
                        game.reset()

                    else:
                        split_data = data.split()
                        instruction = split_data[0]

                        if instruction == "attack":
                            game.update_squares(player, split_data[1], int(split_data[2]))

                        reply = game

                    # here we return the reply to the clients
                    connection.sendall(pickle.dumps(reply))
            else:
                break
        except:
            break

    # here we close the game - deleting the Object and resetting the players
    print("Lost connection...")
    try:
        del game
        print("Closing game...")
    except:
        pass
    players = -1
    connection.close()


# here is the place where we listen for connections
while True:
    _connection, address = s.accept()
    print(f"Connected to: {address}")

    # when a player is connected, we increment their value and initialize the game
    players += 1
    if players == 0:
        game = Game()
    # when the players are 2 - we start the game and they can start playing
    elif players == 1:
        game.initialized = True
        print("Creating a new game...")

    # starting the new thread for every client that is connected
    start_new_thread(threaded_client, (_connection, players))