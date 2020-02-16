import sys
# Fix path on iOS, otherwise can't find relative imports
sys.path.append("/".join(x for x in __file__.split("/")[:-1]))

from elo import rate_1vs1
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivy.properties import BooleanProperty
from boardhelper import BoardHelper
from kivy.utils import platform
from kivy.clock import mainthread
from kivy.core.window import Window
Window.allow_screensaver = False
Window.size = (350, 600)
from player import Player
from kivymd.color_definitions import colors
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
        HOST = self.read_server_ip_file()  # Remote server ip address
        PORT = self.read_port_file()
        print(HOST, PORT)
        self.client = Client(HOST, PORT)

    def change_style(self):
        style = self.theme_cls.theme_style
        if style == 'Dark':
            new_style = 'Light'
        else:
            new_style = 'Dark'
        self.theme_cls.theme_style = new_style

    def get_theme_color(self):
        style = self.theme_cls.theme_style
        accent_hue = self.theme_cls.accent_hue
        return colors[style][accent_hue]


    def get_opp_theme_color(self):
        style = self.theme_cls.theme_style
        if style == 'Dark':
            opp_style = 'Light'
            accent_hue = self.theme_cls.accent_dark_hue
        else:
            opp_style = 'Dark'
            accent_hue = self.theme_cls.accent_light_hue
        return colors[opp_style][accent_hue]


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
        print("Stop")
        self.client.send_message({"command": "disconnect"})
        self.client.server.close()
        self.client.server = None
        print("Stopped")

    def checkmate(self, checkmated_player_color):
        self.player.update_elo_after_match_ends(checkmated_player_color)

    @mainthread
    def lost_connection_to_server(self):
        from kivymd.toast import toast
        toast('Lost connection to the server.')
    @mainthread
    def change_screen(self, screen_name, *args):
        self.root.current = screen_name


if __name__ == "__main__":
    MainApp().run()
