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
        new_blank_piece = ChessPiece(col=piece_moving.col,row=piece_moving.row, source="kingpiece.png")
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
        print("Checking for check")

        # Check for red being in check
        black_pieces = app.board_helper.black_pieces
        attacked_king = app.board_helper.get_widget_by_color_and_type('red', 'king')
        attacked_king = (attacked_king.row, attacked_king.col)
        for piece in black_pieces:
            attacked_squares, not_attacked_squares = piece.get_attacked_squares()
            if attacked_king in attacked_squares:
                print("Red KING IS ATTACKED by", piece.id())
                return True, "red"

        # Check for black king being in check
        red_pieces = app.board_helper.red_pieces
        attacked_king = app.board_helper.get_widget_by_color_and_type('black', 'king')
        attacked_king = (attacked_king.row, attacked_king.col)
        for piece in red_pieces:
            attacked_squares, not_attacked_squares = piece.get_attacked_squares()
            if attacked_king in attacked_squares:
                print("Black KING IS ATTACKED by", piece.id())
                return True, "black"
        return False, ""

    def simulate_board_with_changed_piece_position(self,piece,new_row,new_col):
        print("This doesn't work yet")
        app = App.get_running_app()
        # Get references to previous game state
        board = app.board_helper
        old_row, old_col = piece.row, piece.col
        old_widgets_by_row_and_column = board.widgets_by_row_and_column.copy()

        # Simulate new game state and look for check
        piece.row = new_row
        piece.col = new_col
        board.widgets_by_row_and_column[(new_row, new_col)] = piece
        check_is_in_simulated_game_state, checked_color = self.check_for_check()

        # Change game state back to original state
        piece.row = old_row
        piece.col = old_col
        board.widgets_by_row_and_column = old_widgets_by_row_and_column

        return check_is_in_simulated_game_state


