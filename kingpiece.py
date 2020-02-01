from chesspiece import ChessPiece
from kivy.app import App
from movehelper import NUM_COLS, NUM_ROWS


class KingPiece(ChessPiece):
    piece_type = "king"

    def get_attacked_squares(self):
        app = App.get_running_app()
        row, col, player = self.row, self.col, self.player
        attacked_squares = []
        not_attacked_squares = []
        possible_moves = [(row + 1, col), (row - 1, col), (row, col + 1),
                          (row, col - 1)]
        for move in possible_moves:
            # Make sure the move is inside the palace
            if move[1] > 5:
                # Trying to move to the right of the palace
                continue
            if move[1] < 3:
                # Trying to move to the left of the palace
                continue
            if move[0] < 7 and player == 'red':
                # Trying to move up from palace
                continue
            if move[0] > 2 and player == 'black':
                # Trying to move up from palace
                continue
            # Check for the flying king rule
            pieces_in_same_column = []
            for _row in range(NUM_ROWS):
                print("This flying king check doesn't work exactly")
                piece = app.board_helper.get_widget_at(_row, move[1])
                if piece.piece_type != 'blank':
                    pieces_in_same_column.append(piece)
            if len(pieces_in_same_column) == 1 and pieces_in_same_column[
                0].piece_type == 'king':
                # Illegal move, can't run into a column facing the enemy king
                not_attacked_squares.append(move)

            piece = app.board_helper.get_widget_at(*move)
            if piece:
                if piece.piece_type != 'blank' and piece.player == player:
                    pass
                else:
                    attacked_squares.append(move)
        return attacked_squares, not_attacked_squares
