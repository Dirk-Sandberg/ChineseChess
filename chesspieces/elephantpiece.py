from chesspieces.chesspiece import ChessPiece
from kivy.app import App


class ElephantPiece(ChessPiece):
    piece_type = "elephant"

    def get_attacked_squares(self):
        row, col, player = self.row, self.col, self.player
        app = App.get_running_app()
        king_is_this_players = True if player == 'red' and app.player.is_red or player == 'black' and not app.player.is_red else False
        attacked_squares = []
        not_attacked_squares = []
        possible_moves = [(row + 2, col + 2), (row - 2, col - 2),
                          (row - 2, col + 2), (row + 2, col - 2)]
        for move in possible_moves:
            row_offset = 1 if move[0] > row else -1
            col_offset = 1 if move[1] > col else -1

            blocking_position = (row + row_offset, col + col_offset)
            piece = app.board_helper.get_widget_at(*blocking_position)
            if piece:
                if piece.piece_type != 'blank':
                    # There is a piece blocking the elephant's path
                    not_attacked_squares.append(move)
                    continue

            # Make sure the move is on the proper side of the river
            if move[0] < 5 and king_is_this_players:# and player == 'red':
                # Trying to move up from river
                continue
            if move[0] > 4 and not king_is_this_players:# and player == 'black':
                # Trying to move down from river
                continue

            piece = app.board_helper.get_widget_at(*move)
            if piece:
                if piece.piece_type != 'blank' and piece.player == player:
                    pass
                else:
                    attacked_squares.append(move)
        return attacked_squares, not_attacked_squares
