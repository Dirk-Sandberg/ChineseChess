import sys
# Fix path on iOS, otherwise can't find relative imports
sys.path.append("/".join(x for x in __file__.split("/")[:-1]))

from elo import rate_1vs1
from kivymd.app import MDApp
from screens.gamescreen import GameScreen
from screens.homescreen import HomeScreen
from chesspiece import ChessPiece
from kivy.properties import BooleanProperty
from halfboard import HalfBoard
from boardhelper import BoardHelper
from communications.client import Client
from kivy.core.window import Window
Window.allow_screensaver = False

class MainApp(MDApp):
    board_helper = BoardHelper()
    highlighted_piece = None
    is_animating = BooleanProperty(False)
    is_turn_owner = BooleanProperty(False)

    client = None

    saved_nickname_filename = "nickname.txt"

    def on_start(self):
        HOST = '127.0.0.1'  # Local testing
        HOST = self.read_server_ip_file()  # Remote server ip address
        PORT = self.read_port_file()
        self.client = Client(HOST, PORT)

        # Directories on iOS can be screwed up
        if platform == 'ios':
            self.saved_nickname_filename = self.user_data_dir + "/" + self.saved_nickname_filename

    def read_port_file(self):
        with open("port.txt", "r") as f:
            return f.read()

    def read_server_ip_file(self):
        with open("server_ip", "r") as f:
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



if __name__ == "__main__":
    MainApp().run()
