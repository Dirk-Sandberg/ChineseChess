from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
from kivy.app import App
from kivy.properties import OptionProperty, StringProperty
from availablemoveindicator import AvailableMoveIndicator
from kivy.core.window import Window

class ChessPiece(ButtonBehavior, Image):
    piece_type = OptionProperty("pawn", options=["blank", "rook", "cannon","pawn", "king", "knight", "guard", "elephant"])
    player = StringProperty("black")

    def highlight_moves(self):
        if self.piece_type == "blank":
            return
        app = App.get_running_app()
        board1 = app.root.ids.game_screen.ids.top_board
        board2 = app.root.ids.game_screen.ids.bottom_board

        # Clear all indicators
        for child in board1.walk():
            #if isinstance(child, ChessPiece):
            child.indicator_opacity = 0
        for i in range(5):
            for j in range(9):
                im1 = board1.get_widget_at(i, j)
                print(im1.__class__)
                im1.indicator_opacity = 1

