import socket
import threading
import json
from communications.helper_functions import build_messages
from kivy.app import App
import select
from kivymd.toast import toast
from functools import partial
from kivy.clock import Clock, mainthread

class Client:
    """This is the class that maintains the connection to the remote server. It
    is in charge of sending messages to the server, receiving messages from the
    server, decoding messages from the server, and calling the functions that
    are meant to be called from the server's message.
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    is_host = False
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
        message = ""
        while self.server:
            try:
                print('listening')
                # Wait until a command is received from the server
                message += self.server.recv(2048).decode()
                # If we get multiple commands at once, separate them
                for message in build_messages(message):
                    # Convert the message to a dict format
                    message = json.loads(message)

                    #print("received message", message)
                    # Read and interpret the json data
                    self.interpret(message)
                    message = ""
            except:
                # Json decoder error, message didn't get fully captured
                # try to get more of the message before interpreting it
                pass

    @mainthread
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
            self.app.player.is_red = True
            self.app.change_screen('lobby_screen')
            game_id = message_dict['game_id']
            self.app.player.game_id = game_id
            self.app.root.ids.lobby_screen.set_this_players_nickname_and_elo()
        elif command == 'host_left_lobby':
            # Host left match before the game started
            Clock.schedule_once(partial(self.app.change_screen, 'lobby_browser_screen'), 0)
            toast("Host left the lobby")
        elif command == 'player_left_lobby':
            # Player two left match before the game started
            self.app.root.ids.lobby_screen.player_two_left()
        elif command == 'player_left_match':
            # Either player left match after checkmate
            Clock.schedule_once(partial(self.app.change_screen, 'lobby_browser_screen'), 0)
            toast("The match has ended")
            self.app.root.ids.game_screen.game_over_dialog.dismiss(to_lobby_browser_screen=True)
        elif command == 'player_joined':
            # A new player entered the game room
            # Get nicknames and elos for each player
            app = App.get_running_app()
            nicknames = []
            elos = []
            players = message_dict['players']
            print(message_dict)
            for player in players:
                nickname = player['nickname']
                nicknames.append(nickname)
                elo = player['elo']
                elos.append(elo)
                if nickname != app.player.nickname:
                    app.player.opponent_elo = elo
                    app.player.opponent_nickname = nickname
            print("Need to make sure usernames are unique")
            # Valid game joined
            self.app.change_screen('lobby_screen')
            self.app.root.ids.lobby_screen.set_nicknames_and_elos(nicknames[0], str(elos[0]), nicknames[1], str(elos[1]))

        elif command == 'match_started':
            # Someone pressed the start game button from the lobby screen
            # All players will receive this message.
            # Get the current turn owner (in this case it will be the host)
            self.current_player = message_dict['player_who_owns_turn']
            all_players = message_dict['players']
            # Switch to the game screen
            self.app.change_screen('game_screen')
            self.app.root.ids.game_screen.new_game()
        elif command == "list_lobbies":
            lobbies = message_dict['lobbies']
            self.app.root.ids.lobby_browser_screen.display_lobbies(lobbies)
        elif command == 'piece_moved':
            # Switch whose turn it is to play
            self.app.is_turn_owner = not self.app.is_turn_owner

            from_pos = message_dict['from_pos']
            to_pos = message_dict['to_pos']
            piece_color = message_dict['color']
            game_screen = self.app.root.ids.game_screen
            game_screen.move_piece(*from_pos, *to_pos, piece_color)

        elif command == 'forfeit':
            loser_color = message_dict['loser_color']
            self.app.player.update_elo_after_match_ends(loser_color)
        elif command == 'rematch_requested':
            self.app.root.ids.game_screen.rematch_requested()
            #this needs to be updated
        elif command == 'revoke_rematch_request':
            print("Trying to revoke rematch request")
            self.app.root.ids.game_screen.rematch_request_revoked()



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


