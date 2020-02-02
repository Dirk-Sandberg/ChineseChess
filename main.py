import sys
# Fix path on iOS, otherwise can't find relative imports
sys.path.append("/".join(x for x in __file__.split("/")[:-1]))

from kivymd.app import MDApp
from screens.gamescreen import GameScreen
from screens.homescreen import HomeScreen
from chesspiece import ChessPiece
from kivy.properties import BooleanProperty
from halfboard import HalfBoard
from boardhelper import BoardHelper

class MainApp(MDApp):
    board_helper = BoardHelper()
    highlighted_piece = None
    is_animating = BooleanProperty(False)
    def on_start(self):
        self.theme_cls.theme_style = 'Dark'
    pass


if __name__ == "__main__":
    MainApp().run()
