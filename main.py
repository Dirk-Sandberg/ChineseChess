import sys
# Fix path on iOS, otherwise can't find relative imports
sys.path.append("/".join(x for x in __file__.split("/")[:-1]))

from elo import rate_1vs1
from kivymd.app import MDApp
from kivy.properties import BooleanProperty
from boardhelper import BoardHelper
from kivy.utils import platform
from kivy.clock import mainthread
from kivy.core.window import Window
Window.allow_screensaver = False
Window.size = (350, 600)
from player import Player
from communications.client import Client
from screens.lobbyscreen import LobbyScreen
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


    def checkmate(self, checkmated_player_color):
        print(checkmated_player_color, " loses")
        winner_elo = 1200
        loser_elo = 800
        new_winner_elo, new_loser_elo = rate_1vs1(winner_elo, loser_elo)

    @mainthread
    def change_screen(self, screen_name):
        self.root.current = screen_name


if __name__ == "__main__":
    MainApp().run()
