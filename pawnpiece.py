from chesspiece import ChessPiece
from kivy.app import App
from movehelper import NUM_COLS, NUM_ROWS


class PawnPiece(ChessPiece):
    piece_type = "pawn"

    def get_attacked_squares(self):
        row, col, player = self.row, self.col, self.player
        attacked_squares = []
        not_attacked_squares = []  # From being blocked or flying king rule
        app = App.get_running_app()
        if player == 'black':
            # Pawn can move down but not up
            if row != NUM_ROWS - 1:
                piece = app.board_helper.get_widget_at(row + 1, col)
                if piece.piece_type != 'blank' and piece.player == player:
                    piece.indicator_opacity = 0
                else:
                    attacked_squares.append((row + 1, col))

            # If pawn is past river, can move left and right
            if row > 4:
                piece = app.board_helper.get_widget_at(row, col - 1)
                if piece:
                    if piece.piece_type != 'blank' and piece.player == player:
                        piece.indicator_opacity = 0
                    else:
                        attacked_squares.append((row, col - 1))
                piece = app.board_helper.get_widget_at(row, col + 1)
                if piece:
                    if piece.piece_type != 'blank' and piece.player == player:
                        piece.indicator_opacity = 0
                    else:
                        attacked_squares.append((row, col + 1))


        else:
            # Pawn can move up but not down
            if row != 0:
                piece = app.board_helper.get_widget_at(row - 1, col)
                if piece.piece_type != 'blank' and piece.player == player:
                    piece.indicator_opacity = 0
                else:
                    attacked_squares.append((row - 1, col))

            # If pawn is past river, can move left and right
            if row < 5:
                piece = app.board_helper.get_widget_at(row, col - 1)
                if piece:
                    if piece.piece_type != 'blank' and piece.player == player:
                        piece.indicator_opacity = 0
                    else:
                        attacked_squares.append((row, col - 1))

                piece = app.board_helper.get_widget_at(row, col + 1)
                if piece:
                    if piece.piece_type != 'blank' and piece.player == player:
                        piece.indicator_opacity = 0
                    else:
                        attacked_squares.append((row, col + 1))
        return attacked_squares, not_attacked_squares
