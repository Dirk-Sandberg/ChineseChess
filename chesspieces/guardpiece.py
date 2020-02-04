from chesspieces.chesspiece import ChessPiece
from kivy.app import App


class GuardPiece(ChessPiece):
    piece_type = "guard"

    def get_attacked_squares(self):
        row, col, player = self.row, self.col, self.player
        app = App.get_running_app()
        king_is_this_players = True if player == 'red' and app.player.is_red or player == 'black' and not app.player.is_red else False
        attacked_squares = []
        not_attacked_squares = []
        possible_moves = [(row + 1, col + 1), (row - 1, col - 1),
                          (row - 1, col + 1), (row + 1, col - 1)]
        for move in possible_moves:
            # Make sure the move is inside the palace
            if move[1] > 5:
                # Trying to move to the right of the palace
                continue
            if move[1] < 3:
                # Trying to move to the left of the palace
                continue
            if move[0] < 7 and king_is_this_players:# and player == 'red':
                # Trying to move above palace
                continue
            if move[0] > 2 and not king_is_this_players:# and player == 'black':
                # Trying to move below palace
                continue

            piece = app.board_helper.get_widget_at(*move)
            if piece:
                if piece.piece_type != 'blank' and piece.player == player:
                    pass
                else:
                    attacked_squares.append(move)

        return attacked_squares, not_attacked_squares
