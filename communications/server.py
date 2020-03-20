import socket
from _thread import start_new_thread
from helper_functions import build_messages
import json
from ast import literal_eval
from datetime import datetime
from requests import get, post, patch
from json import dumps
from time import sleep
import asyncio



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
        {"ABCD": [60, 26], "EFGH": [16, 26]}
    Where "ABCD" is the game_id and the integers are the number of seconds for
    the black and red player respectively. Once one number reaches 0, the 
    ticking thread should stop. If a match is forfeited, the ticking thread 
    should stop. The ticking begins when a match starts.
    """
    clocks_by_rooms = {}

    """
    This is a dict with format:
        {"ABCD": 0, "EFGH": 1}
    Contains info about which clock (player) is currently ticking down. Can be
    either 0 or 1. 
    """
    active_clock_by_rooms = {}


    """
    This is a dict with format: 
        {"ip_and_port": {'nickname': 'player1', 'elo': 1200}}
    It's sent as data to the clients so the client can figure out which player
    has what nickname.
    """
    nicknames_for_clients = {}


    """
    This is a list of dicts. Example:
        [{"host_name": "Erik", "host_elo": 1200, "time_limit": 5},
         {"host_name": "Sarah", "host_elo": 1422, "time_limit": 10}]
    """
    lobbies = []

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    next_game_id = '0'

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


    def _clockthread(self, game_id):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.clockthread(game_id))
        #asyncio.run(self.clockthread(game_id))
        """Sends a clock_ticked command.

    async def clockthread(self, game_id):
        Sends a clock_ticked command.

        SLEEPTIME = .05  # Tenth of a second
        time_before = self.clocks_by_rooms[game_id][0]
        print(time_before)
        while True:
            await asyncio.sleep(SLEEPTIME)

        """
    async def clockthread(self, game_id):
        SLEEPTIME = .05  # Tenth of a second
        while True:
            await asyncio.sleep(SLEEPTIME)

            # Remove time from the active clock
            active_clock = self.active_clock_by_rooms[game_id]

            # Check time before and after to see if an integer second has passed
            time_before = self.clocks_by_rooms[game_id][active_clock]


            self.clocks_by_rooms[game_id][active_clock] -= SLEEPTIME
            seconds_remaining = self.clocks_by_rooms[game_id][active_clock]

            if int(time_before) - int(seconds_remaining) == 1:
                # Send new clock times to both clients
                message = {"command": "clock_ticked"}
                clients = self.clients_by_rooms[game_id]
                self.broadcast(message, clients)
                print('tick', datetime.now().second)


            if seconds_remaining <= 0:
                # No longer needs this clockthread
                print("BREAKING CLOCKTHREAD")
                break

    def switch_active_clocks(self, game_id):
        """
        Switch which clock is active for a particular game. Called when this
        server receives a move_piece command, as that signifies the end of one
        player's turn.
        :param game_id: The game room in question
        """
        current_clock = self.active_clock_by_rooms[game_id]
        new_clock = 1 if current_clock == 0 else 0
        self.active_clock_by_rooms[game_id] = new_clock


    def start_new_clockthread(self, game_id, time_limit):
        print("Starting new clockthread")
        # Convert time limit to seconds
        # Initialize the clocks
        # Convert time limit to seconds
        time_limit *= 60
        self.clocks_by_rooms[game_id] = [time_limit, time_limit]

        # the self.clocks_by_rooms variable is set when the match is hosted
        # instead of started
        self.active_clock_by_rooms[game_id] = 0

        # Start the clockthread
        start_new_thread(self._clockthread, (game_id,))

    def end_clockthread(self, game_id):
        """Stops the clockthread by pretending a player's clock is at zero.
        Needs to be called when the game ends via
            checkmate
            disconnect
            forfeit
        :param game_id:
        """
        self.clocks_by_rooms[game_id] = [0, 0]

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
                    received_messages = received_messages.decode()
                    # Separate the messages if more than one was received
                    for received_message in build_messages(received_messages):
                        # Convert the message from a string to a dict object
                        received_message = json.loads(received_message)
                        # Figure out what needs to be done based on the message
                        message_to_send, clients_to_send_to = self.interpret(sender_ip, sender_port, received_message)
                        # Send the message to all the necessary clients
                        self.broadcast(message_to_send, clients_to_send_to)
                else:
                    # Message may have no content if the connection is broken,
                    # in this case we remove the connection
                    self.remove(sender_ip+":"+sender_port, conn)
                    # End the while loop as the connection has closed
                    # This will terminate the thread
                    break
            except IOError as e:
                # Bad file descriptor
                print('Client connection broke, end this client thread')
                break
            except Exception as e:
                print('error in client thread', e, received_messages)
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
        # These commands can be sent from a client that doesn't have a game ID assigned yet
        commands_without_game_id = ['host_match', 'get_lobbies', 'check_nickname_avail', 'disconnect']
        if command not in commands_without_game_id:
            # game_id has been assigned
            game_id = message_dict['from_player']['game_id'].upper()  # Fix upper/lowercase issue
        if command == 'host_match':
            # Someone created a new game room
            # Assign a game id to the room
            game_id = self.next_game_id
            self.next_game_id = str(int(self.next_game_id)+1)
            nickname = message_dict['from_player']['nickname']
            if nickname == "":
                nickname = "Anonymous"
            elo = message_dict['from_player']['elo']
            time_limit = message_dict['time_limit']

            # Keep track of the lobby they created
            lobby = {"host_name": nickname, "host_elo": elo,
                     "time_limit": time_limit, "game_id": game_id}
            self.lobbies.append(lobby)

            # Add the client to the game room
            self.add_client_to_game_room(sender_ip, sender_port, game_id, nickname, elo)

            # Send a message to everyone playing that a new lobby was created
            clients_to_notify = list(self.list_of_clients.keys())
            response_dict = {"command": "list_lobbies", "lobbies": self.lobbies}
            self.broadcast(response_dict, clients_to_notify)


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
                elo = message_dict['from_player']['elo']
                self.add_client_to_game_room(sender_ip, sender_port, game_id,
                                             nickname, elo)
                # Send a message to all players in the room.
                # The message should contain a list of all players currently in
                # the room.
                clients_to_notify = self.clients_by_rooms[game_id]
                players = []
                for client in clients_to_notify:
                    players.append(self.nicknames_for_clients[client])
                # players key should now hold nickname and elo
                response_dict = {"command": "player_joined", "players": players}
                return response_dict, clients_to_notify

        elif command == 'start_match':
            # Since the game started, remove it from the open lobbies list
            for lobby in self.lobbies:
                if lobby['game_id'] == game_id:
                    self.lobbies.remove(lobby)
                else:
                    continue
            time_limit = message_dict['time_limit']

            # Tell all players in a room that a game has started
            clients_to_notify = self.clients_by_rooms[game_id]
            response_dict = {"command": "match_started", "player_who_owns_turn": clients_to_notify[0], "players": clients_to_notify}

            # Start the thread that watches the players' clocks
            print("NEW CLOCKTHREAD ONE")
            self.start_new_clockthread(game_id, time_limit)
            return response_dict, clients_to_notify
        elif command == 'leave_lobby':
            # Called when someone joins a match, then leaves the lobby
            self.clients_by_rooms[game_id].remove(sender)
            sender_was_host = message_dict['is_host']
            if sender_was_host:
                # All players have left the lobby
                # Send a message to the other player that the host left
                if self.clients_by_rooms[game_id] != []:
                    # There is a player in the room that didn't leave
                    clients_to_notify = self.clients_by_rooms[game_id]
                    response_dict = {"command": "host_left_lobby"}
                    self.broadcast(response_dict, clients_to_notify)

                # Send a message to everyone playing that a lobby was removed
                clients_to_notify = list(self.list_of_clients.keys())
                response_dict = {"command": "list_lobbies", "lobbies": self.lobbies}

                self.clients_by_rooms.pop(game_id)
                for lobby in self.lobbies:
                    if lobby['game_id'] == game_id:
                        self.lobbies.remove(lobby)
                    else:
                        continue
                return response_dict, clients_to_notify
            else:
                # Second player to join left the lobby
                clients_to_notify = self.clients_by_rooms[game_id]
                response_dict = {"command": "player_left_lobby"}
            return response_dict, clients_to_notify

        elif command == "get_lobbies":
            # Send the client all the active lobbies
            clients_to_notify = [sender]
            response_dict = {"command": "list_lobbies", "lobbies": self.lobbies}
            return response_dict, clients_to_notify
        elif command == "move_piece":
            # Switch which clock is ticking down.
            self.switch_active_clocks(game_id)
            clients_to_notify = self.clients_by_rooms[game_id]
            response_dict = message_dict
            response_dict['command'] = "piece_moved"
            return response_dict, clients_to_notify
        elif command == 'forfeit':
            # End the clockthread for this game
            self.end_clockthread(game_id)
            clients_to_notify = self.clients_by_rooms[game_id]
            response_dict = message_dict
            return response_dict, clients_to_notify
        elif command == 'checkmate':
            # Someone got checkmated, end the ticking clocks
            self.end_clockthread(game_id)
        elif command == 'rematch_requested':
            clients_to_notify = self.clients_by_rooms[game_id].copy()
            clients_to_notify.remove(sender)
            response_dict = message_dict
            return response_dict, clients_to_notify
        elif command == 'rematch_accepted':
            # Start ticking the clocks again
            time_limit = message_dict['time_limit']
            print("NEW CLOCKTHREAD TWO")
            self.start_new_clockthread(game_id, time_limit)

            # Tell all players in a room that a game has started
            clients_to_notify = self.clients_by_rooms[game_id]
            response_dict = {"command": "match_started",
                             "player_who_owns_turn": clients_to_notify[0],
                             "players": clients_to_notify}
            return response_dict, clients_to_notify
        elif command == 'revoke_rematch_request':
            clients_to_notify = self.clients_by_rooms[game_id].copy()
            clients_to_notify.remove(sender)
            response_dict = message_dict
            return response_dict, clients_to_notify

        elif command == "leave_match":
            # Someone left the game after match ended occurred
            response_dict = {"command": "player_left_match"}
            # This might occur after the other player disconnected before checkmate
            # If so, clients_by_rooms[game_id] will give an exception as it was popped already
            try:
                clients_to_notify = self.clients_by_rooms[game_id].copy()
                clients_to_notify.remove(sender)
                self.clients_by_rooms.pop(game_id)
            except:
                clients_to_notify = []
                pass
            return response_dict, clients_to_notify

        elif command == 'disconnect':
            # Client will be closed automatically when it doesn't receive the
            # next message
            self.remove(sender, self.list_of_clients[sender])
            return "", []  # Don't send any messages to anyone
        elif command == 'check_nickname_avail':
            r = get('https://chinese-chess-6543e.firebaseio.com/nicknames.json')
            str_names = r.content.decode()
            print(str_names)
            str_names = str_names.replace('"',"")
            names = str_names.split(",")
            print(names)
            name_to_check = message_dict['nickname']
            if name_to_check in names:
                response_dict = {'command': 'invalid_nickname'}
            else:
                response_dict = {'command': 'valid_nickname'}
                # Update firebase with new nickname
                str_names += ',' + name_to_check
                new_names = {'nicknames': str_names}
                r = patch('https://chinese-chess-6543e.firebaseio.com/.json',
                         data=dumps(new_names))
            return response_dict, [sender]


    def add_client_to_game_room(self, client_ip, client_port, game_id, nickname, elo):
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
            player_info = {}
            player_info['nickname'] = proper_nickname
            player_info['elo'] = elo
            # Keep track of the nickname for this client
            self.nicknames_for_clients[client_ip + ":" + client_port] = player_info
        except KeyError:
            # This is the first player entering a new game room
            # Need to create a new key in the self.clients_by_rooms dict
            self.clients_by_rooms[game_id] = [client_ip + ":" + client_port]

            # If the user didn't specify a nickname, set nickname to Player 1
            if nickname == "":
                proper_nickname = "Player 1"
            else:
                proper_nickname = nickname
            player_info = {}
            player_info['nickname'] = proper_nickname
            player_info['elo'] = elo

            # Keep track of the nickname for this client
            self.nicknames_for_clients[client_ip + ":" + client_port] = player_info


    def broadcast(self, message, list_of_clients):
        """Sends a single message to a group of clients.

        :param message: The message to send. Type is dict
        :param list_of_clients: The list of ip_and_port strings to send to
        :return:
        """
        print("Trying to broadcast")
        for ip_and_port in list_of_clients:
            print("broadcasting to:", ip_and_port)
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
                print("Couldn't send message, going to remove client!", e)
                self.remove(ip_and_port, client)


    def remove(self, ip_and_port, connection):
        """Remove all references to the client that is being removed, and close
        that connection.
        """
        print("Trying to remove:", ip_and_port)
        try:
            self.list_of_clients.pop(ip_and_port)  # Remove client from dictionary
            self.nicknames_for_clients.pop(ip_and_port) # Forget nickname for client
            # Remove this client from the clients by rooms dict
            for game_id, client_ip_and_ports in self.clients_by_rooms.items():  # for name, age in dictionary.iteritems():  (for Python 2.x)
                if ip_and_port in client_ip_and_ports:
                    print("Client is in game room: ", game_id)
                    # GOT THE PROPER GAME ID
                    # The player is either in a lobby or a match

                    # Check if they're in a lobby
                    # - If they are:
                    # -- remove them from clients_by_game_rooms
                    # -- close lobby if they weren't the host
                    # Try to remove this player's lobby from the open lobbies list
                    player_was_in_lobby = False
                    for lobby in self.lobbies:
                        if lobby['game_id'] == game_id:
                            # Player was in a lobby
                            player_was_in_lobby = True
                            # Remove them from the lobby
                            index = self.clients_by_rooms[game_id].index(ip_and_port)
                            was_host = True if index == 0 else False
                            self.clients_by_rooms[game_id].remove(ip_and_port)
                            # Remove the lobby entirely if it's empty now
                            if was_host:
                                # If there was a second player, tell them to leave the lobby
                                clients_to_notify = self.clients_by_rooms[game_id]
                                response_dict = {"command": "player_left_lobby"}
                                self.broadcast(response_dict, clients_to_notify)

                                # Remove the lobby
                                # Remove the room from clients by rooms
                                self.lobbies.remove(lobby)
                                self.clients_by_rooms.pop(game_id)

                                response_dict = {"command": "list_lobbies",
                                                 "lobbies": self.lobbies}
                                # Send a message to all clients that a lobby was removed
                                self.broadcast(response_dict, list(self.list_of_clients.keys()))

                            else:
                                # Second player to join left the lobby
                                clients_to_notify = self.clients_by_rooms[game_id]
                                response_dict = {"command": "player_left_lobby"}
                                self.broadcast(response_dict, clients_to_notify)
                        else:
                            continue
                    # Check if they're in a match
                    # - If they are:
                    # -- remove the game id from clients_by_rooms
                    # -- stop the clock ticking on the server
                    # -- tell other player the match ended
                    # -- (deduct elo)
                    player_was_in_match = not player_was_in_lobby
                    if player_was_in_match:
                        self.clients_by_rooms[game_id].remove(ip_and_port)
                        # Someone disconnected during the middle of a game
                        response_dict = {"command": "player_left_match"}
                        clients_to_notify = self.clients_by_rooms[game_id]
                        # Stop the clockthread for this game
                        self.end_clockthread(game_id)
                        # The match is completely over, so remove that key from clients_by_rooms
                        self.clients_by_rooms.pop(game_id)
                        self.broadcast(response_dict, clients_to_notify)
        except Exception as e:
            # Won't work if they close the app before joining or starting a game
            print('issue removing client', e)

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
