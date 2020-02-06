import sys
# Fix path on iOS, otherwise can't find relative imports
sys.path.append("/".join(x for x in __file__.split("/")[:-1]))

from elo import rate_1vs1
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivy.properties import BooleanProperty
from boardhelper import BoardHelper
from kivy.utils import platform
from gameoverdialog import GameOverDialog
from kivy.clock import mainthread
from kivy.core.window import Window
Window.allow_screensaver = False
Window.size = (350, 600)
from player import Player
from communications.client import Client
from screens.lobbyscreen import LobbyScreen
from screens.setnicknamescreen import SetNicknameScreen
from screens.homescreen import HomeScreen
from screens.gamescreen import GameScreen
from screens.creategamescreen import CreateGameScreen
from screens.lobbybrowserscreen import LobbyBrowserScreen
from halfboard import HalfBoard

class MainApp(MDApp):
    board_helper = BoardHelper()
    highlighted_piece = None
    is_animating = BooleanProperty(False)
    is_turn_owner = BooleanProperty(False)

    # The player class will have its data updated when playing a game
    player = Player()

    client = None

    firebase_url = "https://chinese-chess-6543e.firebaseio.com/"

    def on_login(self):
        pass

    def on_start(self):
        HOST = '127.0.0.1'  # Local testing
        #HOST = self.read_server_ip_file()  # Remote server ip address
        PORT = self.read_port_file()
        print("not connecting to server")
        self.client = Client(HOST, PORT)



    def read_port_file(self):
        with open("port.txt", "r") as f:
            port = f.read()
            return int(port)

    def read_server_ip_file(self):
        with open("server_ip.txt", "r") as f:
            return f.read()

    def on_stop(self):
        """on_stop is automatically called when the app is closed.
        """
        self.client.send_message({"command": "disconnect"})
        self.client.server.close()

    def update_elo_after_match_ends(self, checkmated_player_color):
        if checkmated_player_color == 'red' and self.player.is_red or checkmated_player_color == 'black' and not self.player.is_red:
            loser_elo = self.player.elo
            winner_elo = self.player.opponent_elo
        else:
            loser_elo = self.player.opponent_elo
            winner_elo = self.player.elo
        #host doesn't set opponents elo
        print("AA", winner_elo, loser_elo)
        new_winner_elo, new_loser_elo = rate_1vs1(winner_elo, loser_elo)
        print("BB", new_winner_elo, new_loser_elo)

        # Update the player's elo in firebase.
        if checkmated_player_color == 'red' and self.player.is_red or checkmated_player_color == 'black' and not self.player.is_red:
            new_elo = new_loser_elo
        else:
            new_elo = new_winner_elo
        self.player.set_elo(new_elo)

        g = GameOverDialog(loser_elo, new_loser_elo, winner_elo, new_winner_elo)
        g.open()

    def checkmate(self, checkmated_player_color):
        m = MDDialog(title="CHECKMATE",
                     text=checkmated_player_color + " IS IN CHECKMATE")
        m.open()

        self.update_elo_after_match_ends(checkmated_player_color)


    @mainthread
    def change_screen(self, screen_name):
        self.root.current = screen_name


if __name__ == "__main__":
    MainApp().run()
