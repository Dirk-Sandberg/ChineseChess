from kivy.uix.gridlayout import GridLayout
from kivy.properties import NumericProperty
from chesspiece import ChessPiece
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.animation import Animation
from rookpiece import RookPiece
from guardpiece import GuardPiece
from elephantpiece import ElephantPiece
from knightpiece import KnightPiece
from pawnpiece import PawnPiece
from kingpiece import KingPiece
from cannonpiece import CannonPiece

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
                        c = RookPiece(player=self.player_color)
                    elif col == 1 or col == (self.cols-2):
                        c = KnightPiece(player=self.player_color)
                    elif col == 2 or col == (self.cols - 3):
                        c = ElephantPiece(player=self.player_color)
                    elif col == 3 or col == (self.cols-4):
                        c = GuardPiece(player=self.player_color)
                    elif col == 4:
                        c = KingPiece(player=self.player_color)
                elif row == 2:
                    # Add cannons
                    if col == 1 or col == (self.cols-2):
                        c = CannonPiece(player=self.player_color)
                elif row == pawn_row:
                    # Add pawns
                    if col in [0, 2, 4, 6, 8]:
                        c = PawnPiece(player=self.player_color)
                if not c:
                    c = ChessPiece(piece_type="blank")
                c.opacity = 0
                c.row, c.col = board_helper.convert_to_global_indices(row, col, self.half)
                #c.col = col
                c.board_half = self.half
                self.add_widget(c)

                if c.piece_type != 'blank':
                    if self.player_color == 'black':
                        board_helper.black_pieces.append(c)
                    else:
                        board_helper.red_pieces.append(c)
                board_helper.widgets_by_row_and_column[(c.row, c.col)] = c
                board_helper.row_and_column_by_widget["%s:%s"%(c.player,c.piece_type)] = (c.row, c.col)

        # Animate all the pieces into view
        anim = Animation(opacity=1)
        for child in self.walk():
            if isinstance(child, ChessPiece):
                anim.start(child)





