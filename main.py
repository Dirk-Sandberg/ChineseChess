from kivymd.app import MDApp
from screens.gamescreen import GameScreen
from screens.homescreen import HomeScreen
from chesspiece import ChessPiece
from halfboard import HalfBoard
from boardhelper import BoardHelper

class MainApp(MDApp):
    board_helper = BoardHelper()
    highlighted_piece = None
    pass


if __name__ == "__main__":
    MainApp().run()
