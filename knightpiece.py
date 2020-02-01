from chesspiece import ChessPiece
from kivy.app import App
from movehelper import NUM_COLS, NUM_ROWS


class KnightPiece(ChessPiece):
    piece_type = "knight"

    def get_attacked_squares(self):
        app = App.get_running_app()
        row, col, player = self.row, self.col, self.player
        attacked_squares = []
        not_attacked_squares = []
        possible_moves = [(row + 1, col + 2), (row + 1, col - 2),
                          (row + 2, col + 1), (row + 2, col - 1),
                          (row - 1, col + 2), (row - 1, col - 2),
                          (row - 2, col + 1), (row - 2, col - 1)]
        for move in possible_moves:
            row_offset = 0 if abs(move[0] - row) < 2 else int(
                (move[0] - row) / 2)
            col_offset = 0 if abs(move[1] - col) < 2 else int(
                (move[1] - col) / 2)
            blocking_position = (row + row_offset, col + col_offset)
            blocking_piece = app.board_helper.get_widget_at(*blocking_position)
            if blocking_piece:
                if blocking_piece.piece_type != 'blank':
                    # There is a piece blocking the knight's path
                    not_attacked_squares.append(move)
                    print("Knight is being blocked by", blocking_piece)
                    continue

            piece = app.board_helper.get_widget_at(*move)
            if piece:
                if piece.piece_type != 'blank' and piece.player == player:
                    pass
                else:
                    attacked_squares.append(move)
        return attacked_squares, not_attacked_squares
