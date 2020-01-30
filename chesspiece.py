from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
from kivy.app import App
from kivy.properties import OptionProperty, StringProperty
from movehelper import highlight_rook_moves
from availablemoveindicator import AvailableMoveIndicator
from kivy.core.window import Window

class ChessPiece(ButtonBehavior, Image):
    piece_type = OptionProperty("pawn", options=["blank", "rook", "cannon","pawn", "king", "knight", "guard", "elephant"])
    player = StringProperty("black")

    def highlight_moves(self):
        app = App.get_running_app()
        board1 = app.root.ids.game_screen.ids.top_board
        board2 = app.root.ids.game_screen.ids.bottom_board

        # If they clicked on a blank spot, move their piece
        if self.piece_type == "blank":
            if self.indicator_opacity == 1:
                self.piece_type = app.highlighted_piece.piece_type
                self.player = app.highlighted_piece.player
                app.highlighted_piece.piece_type = 'blank'
            # Clear all indicators
            for child in board1.walk():
                child.indicator_opacity = 0
            for child in board2.walk():
                child.indicator_opacity = 0
            return

        else:
            app.highlighted_piece = self
        # Clear all indicators
        for child in board1.walk():
            child.indicator_opacity = 0
        for child in board2.walk():
            child.indicator_opacity = 0


        if self.piece_type == "rook":
            highlight_rook_moves(self.row, self.col, self.player)

