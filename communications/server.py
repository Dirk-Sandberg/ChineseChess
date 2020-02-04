import socket
from _thread import start_new_thread
from helper_functions import build_messages
import json
from ast import literal_eval

class Server:
    """This is the class that maintains the connections to the remote clients.
    It creates a new thread for every client that connects. Each thread listens
    for messages from the client, decodes and interprets the message, and sends
    a response tailored to what the received message was.
    """

    """ 
    This is a dict with format: {"client_ip_and_port": ConnectionObject}
    It lets us refer to a clients connection just by know the client's
    ip and port
    """
    list_of_clients = {}

    """
    This is a dict with format: 
        {"ABCD": ['client_ip_and_port1', 'client_ip_and_port2']}
    It lets us get references to all players inside of one game room
    """
    clients_by_rooms = {}

    """
    This is a dict with format: 
        {"ip_and_port": 'nickname'}
    It's sent as data to the clients so the client can figure out which player
    has what nickname.
    """
    nicknames_for_clients = {}  # e.g. {"192.168.2.4:60124": "player1"}


    """
    This is a list of dicts. Example:
        [{"host_name": "Erik", "host_elo": 1200, "time_limit": 5},
         {"host_name": "Sarah", "host_elo": 1422, "time_limit": 10}]
    """
    lobbies = []

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self):
        """The first argument AF_INET is the address domain of the
        socket. This is used when we have an Internet Domain with
        any two hosts. The second argument is the type of socket.
        SOCK_STREAM means that data or characters are read in
        a continuous flow."""
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        host = '0.0.0.0'
        """
        Open the server on port xxxxx. This port number must be known by all 
        clients
        """
        with open("port.txt", "r") as f:
            port = int(f.read())

        """ 
        Bind the server to an entered IP address and at the specified port
        number. The client must be aware of these parameters 
        """
        self.server.bind((host, port))

        """ 
        Listen for 100 active connections (clients). This number can be 
        increased as per convenience. 
        """
        self.server.listen(100)

    def clientthread(self, conn, addr):
        """Pauses the thread while waiting for a command from this particular
        client. If a command is received, it will decode the message(s) from
        bytes to a dict type object (json data), then call the :interpret:
        function to figure out what commands need to be sent back and to which
        client(s) they need to be sent.
        Repeats infinitely.
        """
        while True:
            try:
                # Pause this thread until a message is received from the client
                received_messages = conn.recv(2048)
                sender_ip = addr[0]
                sender_port = str(addr[1])
                if received_messages:
                    print("Got message(s)", received_messages)
                    print("Z")
                    received_messages = received_messages.decode()
                    print("X")
                    # Separate the messages if more than one was received
                    for received_message in build_messages(received_messages):
                        # Convert the message from a string to a dict object
                        print("zz", received_message)
                        received_message = json.loads(received_message)
                        print("Y")
                        # Figure out what needs to be done based on the message
                        message_to_send, clients_to_send_to = self.interpret(sender_ip, sender_port, received_message)

                        # Send the message to all the necessary clients
                        self.broadcast(message_to_send, clients_to_send_to)

                else:
                    print("Didnt get message")
                    # Message may have no content if the connection is broken,
                    # in this case we remove the connection
                    self.remove(sender_ip+":"+sender_port, conn)
                    # End the while loop as the connection has closed
                    # This will terminate the thread
                    break

            except Exception as e:
                print('error in client thread', e)
                print("Client thread error -- message", received_messages)
                continue

    def interpret(self, sender_ip, sender_port, message_dict):
        """This is where the server reads what it was sent and builds a
        response.

        :param sender_ip: The ip address of the client who sent the message
        :param sender_port: The port that the client is sending messages from
        :param message_dict: dict type which always contains at least two keys,
        the 'command' and the 'game_id'. It contains special data relevant to
        the command that was sent. The message_dict is exactly what the client
        sent in the Client's send_message function.

        :return: Two variables -- one is the dict message to send in response,
        the other is the list of clients to send to.
        """
        command = message_dict['command']
        sender = sender_ip + ":" + sender_port
        if command != 'host_match' and command != 'get_lobbies':
            # game_id has been assigned
            game_id = message_dict['from_player']['game_id'].upper()  # Fix upper/lowercase issue
        if command == 'host_match':
            # Someone created a new game room
            # Assign a game id to the room
            game_id = 'AA'
            nickname = message_dict['from_player']['nickname']
            elo = message_dict['from_player']['elo']
            time_limit = message_dict['time_limit']

            # Keep track of the lobby they created
            lobby = {"host_name": nickname, "host_elo": elo,
                     "time_limit": time_limit, "game_id": game_id}
            self.lobbies.append(lobby)

            # Add the client to the game room
            self.add_client_to_game_room(sender_ip, sender_port, game_id, nickname)
            # Send a message back saying they succeeded in creating the room
            response_dict = {"command": "match_hosted", "game_id": game_id}
            clients_to_notify = [sender]
            return response_dict, clients_to_notify

        elif command == 'join_game':
            # Someone is trying to join a game. Check if their game id is valid
            active_games = list(self.clients_by_rooms.keys())
            if game_id not in active_games:
                # Send a message back saying the game id was invalid
                response_dict = {"command": "invalid_game_id"}
                clients_to_notify = [sender]
                return response_dict, clients_to_notify
            else:
                # The game id does exist. Add them to the room
                nickname = message_dict['from_player']['nickname']
                self.add_client_to_game_room(sender_ip, sender_port, game_id,
                                             nickname)
                # Send a message to all players in the room.
                # The message should contain a list of all players currently in
                # the room.
                clients_to_notify = self.clients_by_rooms[game_id]
                response_dict = {"command": "player_joined", "players": list(self.nicknames_for_clients.values())}
                return response_dict, clients_to_notify

        elif command == 'start_match':
            # Since the game started, remove it from the open lobbies list
            #self.lobbies.remove(lobby)
            print("Should remove lobby here")
            # Tell all players in a room that a game has started
            clients_to_notify = self.clients_by_rooms[game_id]
            response_dict = {"command": "match_started", "player_who_owns_turn": clients_to_notify[0], "players": clients_to_notify}

            return response_dict, clients_to_notify

        elif command == "get_lobbies":
            # Send the client all the active lobbies
            clients_to_notify = [sender]
            response_dict = {"command": "list_lobbies", "lobbies": self.lobbies}
            return response_dict, clients_to_notify
        elif command == "move_piece":
            clients_to_notify = self.clients_by_rooms[game_id]
            response_dict = message_dict
            response_dict['command'] = "piece_moved"
            return response_dict, clients_to_notify


        elif command == 'disconnect':
            # Client will be closed automatically when it doesn't receive the
            # next message
            try:
                self.clients_by_rooms[game_id].remove(sender)
                if self.clients_by_rooms[game_id] == []:
                    # If there are no players remaining, free up the game id
                    self.clients_by_rooms.pop(game_id)
            except:
                # Client wasn't in a room yet.
                pass

    def add_client_to_game_room(self, client_ip, client_port, game_id, nickname):
        """Keeps track of the players that are attached to each game room. Does
        so by adding the player to the :self.clients_by_rooms: dict under the
        :game_id:'s key in the dict.

        If the :game_id: doesn't exist as a key in :self.clients_by_rooms: a new
        key will be added for this :game_id:

        :param client_ip: The ip address of the client
        :param client_port: The port the client is using
        :param game_id: The game id of the room to be joined by the client
        :param nickname: A nickname for the client
        :return:
        """
        try:
            # Fails if there is no game id key in self.clients_by_rooms
            self.clients_by_rooms[game_id].append(client_ip + ":" + client_port)
            num_players = len(self.clients_by_rooms[game_id])

            # If the user didn't specify a nickname, set nickname to Player X
            if nickname == "":
                proper_nickname = "Player %s"%num_players
            else:
                proper_nickname = nickname

            # Keep track of the nickname for this client
            self.nicknames_for_clients[client_ip + ":" + client_port] = proper_nickname
        except KeyError:
            # This is the first player entering a new game room
            # Need to create a new key in the self.clients_by_rooms dict
            self.clients_by_rooms[game_id] = [client_ip + ":" + client_port]

            # If the user didn't specify a nickname, set nickname to Player 1
            if nickname == "":
                proper_nickname = "Player 1"
            else:
                proper_nickname = nickname

            # Keep track of the nickname for this client
            self.nicknames_for_clients[client_ip + ":" + client_port] = proper_nickname


    def broadcast(self, message, list_of_clients):
        """Sends a single message to a group of clients.

        :param message: The message to send. Type is dict
        :param list_of_clients: The list of ip_and_port strings to send to
        :return:
        """
        for ip_and_port in list_of_clients:
            # Get a reference to the actual client connection using their
            # ip and port
            client = self.list_of_clients[ip_and_port]

            # If the message contains info about whose turn it is, give a
            # special message to the person whose turn it is so they know
            player_who_owns_turn = message.get("player_who_owns_turn", "")
            if player_who_owns_turn:
                # There's info about whose turn it is in the message
                if ip_and_port == player_who_owns_turn:
                    message['turn_owner'] = True
                else:
                    message['turn_owner'] = False

            try:
                client.send(json.dumps(message).encode())
            except Exception as e:
                # If the connection is broken, we remove the client
                print("Couldn't send message", e)
                self.remove(ip_and_port, client)


    def remove(self, ip_and_port, connection):
        """Remove all references to the client that is being removed, and close
        that connection.
        """
        try:
            self.list_of_clients.pop(ip_and_port)  # Remove client from dictionary
            self.nicknames_for_clients.pop(ip_and_port) # Forget nickname for client
        except:
            # Won't work if they close the app before joining or starting a game
            pass
        connection.close()
        print("Closed connection from", ip_and_port)

    def run(self):
        """The function being run by the server in the main thread. This listens
        for new connections, and if it receives one, it starts a new thread for
        the client that connected. The thread runs the :self.clientthread:
        function.
        """
        while True:
            """
            Wait for a connection request and store two parameters, conn 
            which is a socket object for that user, and addr which contains the
            IP address and port number of the client that just connected
            """
            conn, addr = self.server.accept()

            """
            Maintains a list of clients for ease of broadcasting a message to 
            all players in a game room.
            """
            ip, port = addr[0], str(addr[1])
            self.list_of_clients[ip + ":" + port] = conn
            print(ip + ":" + port + " connected")

            # Create an individual thread for every user that connects
            start_new_thread(self.clientthread, (conn, addr))

        conn.close()
        server.close()


Server().run()
