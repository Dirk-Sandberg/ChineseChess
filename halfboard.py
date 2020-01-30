from kivy.uix.gridlayout import GridLayout
from kivy.properties import NumericProperty
from chesspiece import ChessPiece
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.animation import Animation

class HalfBoard(GridLayout):
    rows = NumericProperty(5)
    cols = NumericProperty(9)

    def add_starting_pieces(self):
        board_helper = App.get_running_app().board_helper
        if self.half == "top":
            back_row = 0
            pawn_row = 3
        else:
            back_row = self.rows-1
            pawn_row = self.rows-4

        for row in range(self.rows):
            for col in range(self.cols):
                c = None
                if row == back_row:
                    # Set back row pieces
                    if col == 0 or col == (self.cols-1):
                        c = ChessPiece(piece_type="rook", player=self.player_color)
                    elif col == 1 or col == (self.cols-2):
                        c = ChessPiece(piece_type="knight", player=self.player_color)
                    elif col == 2 or col == (self.cols - 3):
                        c = ChessPiece(piece_type="elephant", player=self.player_color)
                    elif col == 3 or col == (self.cols-4):
                        c = ChessPiece(piece_type="guard", player=self.player_color)
                    elif col == 4:
                        c = ChessPiece(piece_type="king", player=self.player_color)
                elif row == 2:
                    # Add cannons
                    if col == 1 or col == (self.cols-2):
                        c = ChessPiece(piece_type="cannon", player=self.player_color)
                elif row == pawn_row:
                    # Add pawns
                    if col in [0, 2, 4, 6, 8]:
                        c = ChessPiece(piece_type="pawn", player=self.player_color)
                if not c:
                    c = ChessPiece(piece_type="blank")
                c.opacity = 0
                c.row, c.col = board_helper.convert_to_global_indices(row, col, self.half)
                #c.col = col
                c.board_half = self.half
                self.add_widget(c)

                board_helper.widgets_by_row_and_column[(c.row, c.col)] = c
                board_helper.row_and_column_by_widget[c] = (c.row, c.col)

        # Animate all the pieces into view
        anim = Animation(opacity=1)
        for child in self.walk():
            if isinstance(child, ChessPiece):
                anim.start(child)





