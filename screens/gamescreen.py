from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.properties import BooleanProperty
from movehelper import NUM_ROWS, NUM_COLS
from rookpiece import RookPiece
from chesspiece import ChessPiece

class GameScreen(Screen):
    online_mode_enabled = BooleanProperty(False)

    def move_pieces(self, piece_being_entered_upon, piece_moving):
        # Replace the widget being moved on
        # Place a blank widget where the moving piece left
        to_parent = piece_being_entered_upon.parent
        from_parent = piece_moving.parent
        moving_from = from_parent.children.index(piece_moving)
        moving_to = to_parent.children.index(piece_being_entered_upon)

        # Account for rearranging of widgets in the gridlayout
        if to_parent == from_parent:
            if moving_from < moving_to:
                moving_to -= 1

        from_parent.remove_widget(piece_moving)
        to_parent.remove_widget(piece_being_entered_upon)
        to_parent.add_widget(piece_moving, moving_to)
        new_blank_piece = ChessPiece(col=piece_moving.col,row=piece_moving.row)
        from_parent.add_widget(new_blank_piece, moving_from)
        piece_moving.row = piece_being_entered_upon.row
        piece_moving.col = piece_being_entered_upon.col

        # Update the references to widgets by their col and row in board helper
        app = App.get_running_app()
        board = app.board_helper
        board.widgets_by_row_and_column[(piece_moving.row, piece_moving.col)] = piece_moving
        board.widgets_by_row_and_column[(new_blank_piece.row, new_blank_piece.col)] = new_blank_piece


    def check_for_check(self):
        app = App.get_running_app()

        # Check for red being in check
        black_pieces = app.board_helper.black_pieces
        attacked_king = app.board_helper.get_widget_indices('red', 'king')
        for piece in black_pieces:
            attacked_squares, not_attacked_squares = [], []
            if attacked_king in attacked_squares:
                print("RED KING IS ATTACKED")

        # Check for black king being in check
        red_pieces = app.board_helper.red_pieces
        attacked_king = app.board_helper.get_widget_indices('black', 'king')
        for piece in red_pieces:
            attacked_squares, not_attacked_squares = [], []
            if attacked_king in attacked_squares:
                print("Black KING IS ATTACKED")


    def move_violates_flying_king_rule(self, row_leaving, row_entering,
                                       col_leaving, col_entering, player):
        app = App.get_running_app()
        king_position = app.board_helper.get_widget_indices(player, 'king')
        print(king_position)
        return False
        pieces_in_same_column = []
        for _row in range(NUM_ROWS):
            piece = app.board_helper.get_widget_at(_row, move[1])
            if piece.piece_type != 'blank':
                pieces_in_same_column.append(piece)
        if len(pieces_in_same_column) == 1 and pieces_in_same_column[
            0].piece_type == 'king':
            # Illegal move, can't run into a column facing the enemy king
            pass


