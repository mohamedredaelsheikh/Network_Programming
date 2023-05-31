import socket
from _thread import *
import pickle
from game import Game

# Server setup
server = "127.0.0.1"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen(2)
print("Waiting for a connection, Server Started")

connected = set()
games = {}
idCount = 0


def threaded_client(conn, player, gameId):
    global idCount
    conn.send(str.encode(str(player)))

    reply = ""
    while True:
        try:
            # Receive data from the client
            data = conn.recv(4096).decode()

            if gameId in games:
                # Retrieve the game object for the specified game ID
                game = games[gameId]

                if not data:
                    break
                else:
                    if data == "reset":
                        # Reset the "went" status of the game
                        game.resetWent()
                    elif data != "get":
                        # Process the player's move
                        game.play(player, data)

                    # Send the updated game object back to the client
                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    print("Lost connection")
    try:
        # Clean up the game and close the connection
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()


while True:
    # Accept incoming connections
    conn, addr = s.accept()
    print("Connected to:", addr)

    idCount += 1
    p = 0
    gameId = (idCount - 1)//2

    if idCount % 2 == 1:
        # Create a new game if the number of players is odd
        games[gameId] = Game(gameId)
        print("Creating a new game...")
    else:
        # Mark the game as ready and set player number if the number of players is even
        games[gameId].ready = True
        p = 1

    # Start a new thread to handle the client connection
    start_new_thread(threaded_client, (conn, p, gameId))
