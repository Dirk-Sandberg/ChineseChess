import socket
import threading
import json
from communications.helper_functions import build_messages
from kivy.app import App
import select


class Client:
    """This is the class that maintains the connection to the remote server. It
    is in charge of sending messages to the server, receiving messages from the
    server, decoding messages from the server, and calling the functions that
    are meant to be called from the server's message.
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    app = None  # A reference to the main App class
    game_id = ""  # Always send the game id as part of the message to the server
    current_player = ""  # Ip and port of the player whose turn it is

    def __init__(self, host, port):
        # Connect to the server
        self.server.connect((host, port))
        # This is just so I can replace App.get_running_app() with self.app
        self.app = App.get_running_app()
        # Start the function that interacts with the server in a new thread
        # without using threading, the app will freeze
        x = threading.Thread(target=self.listen)
        x.start()

    def listen(self, *args):
        """Pauses the thread while waiting for a command from the server. If it
        receives a command, it will decode the message(s) from bytes to a dict
        type object (json data), then call the :interpret: function to figure
        out what needs to be done. Repeats infinitely.
        """
        while True:
            # Wait until a command is received from the server
            message = self.server.recv(2048).decode()
            # If we get multiple commands at once, separate them
            for message in build_messages(message):
                # Convert the message to a dict format
                message = json.loads(message)

                print("received message", message)
                # Read and interpret the json data
                self.interpret(message)

    def interpret(self, message_dict):
        """Figure our the main command the server sent. Then, based on what that
        command is, get other relevant pieces of data from the message. Finally,
        do some work on the screen (e.g. start a game, add a new card).

        :param message_dict: the json data from the server
        """
        command = message_dict['command']

        if command == 'match_hosted':
            # The host is the player who goes first
            self.app.is_turn_owner = True
            self.app.root.current = 'lobby_screen'

        elif command == 'player_joined':
            # A new player entered the game room
            # Get all of the players ip:port combinations
            all_players = message_dict['players']
            # Get nicknames for each player
            nicknames = message_dict['nicknames']
            # Valid game joined

        elif command == 'start_game':
            # Someone pressed the start game button from the lobby screen
            # All players will receive this message.
            # Get the current turn owner (in this case it will be the host)
            self.current_player = message_dict['player_who_owns_turn']
            all_players = message_dict['players']
            # Switch to the game screen
            self.app.root.current = 'game_screen'

        elif command == 'invalid_game_id':
            # This player tried to join a game with an invalid game id
            pass

    def send_message(self, message):
        """Sends a message to the server. All messages should include info about
        the player sending the message.

        :param message: dictionary format (json data)
        """
        #message['game_id'] = self.game_id
        message['from_player'] = self.app.player.__dict__
        # To send the message over the socket connection, convert the message to
        # a string of bytes
        self.server.send(json.dumps(message).encode())

