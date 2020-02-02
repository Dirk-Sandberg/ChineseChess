from chesspiece import ChessPiece
from kivy.app import App
from movehelper import NUM_COLS, NUM_ROWS


class RookPiece(ChessPiece):
    piece_type = "rook"

    def get_attacked_squares(self):
        row, col, player = self.row, self.col, self.player
        attacked_squares = []
        not_attacked_squares = []  # From being blocked or flying king rule
        app = App.get_running_app()
        # Find Available moves down
        # down means increasing row
        has_collided = False
        for _row in range(row + 1, NUM_ROWS):
            if not has_collided:
                piece = app.board_helper.get_widget_at(_row, col)
                if piece.piece_type != 'blank':
                    has_collided = True
                if piece.piece_type != 'blank' and piece.player == player:
                    continue
                    #piece.indicator_opacity = 0
                else:
                    attacked_squares.append((_row, col))

        # Find Available moves up
        # up means decreasing row
        has_collided = False
        for _row in range(0, row)[::-1]:
            if not has_collided:
                piece = app.board_helper.get_widget_at(_row, col)
                if piece.piece_type != 'blank':
                    has_collided = True
                if piece.piece_type != 'blank' and piece.player == player:
                    continue
                    #piece.indicator_opacity = 0
                else:
                    attacked_squares.append((_row, col))

        # Find Available moves left
        # left means decreasing column
        has_collided = False
        for _col in range(0, col)[::-1]:
            if not has_collided:
                piece = app.board_helper.get_widget_at(row, _col)
                if piece.piece_type != 'blank':
                    has_collided = True
                if piece.piece_type != 'blank' and piece.player == player:
                    continue
                    #piece.indicator_opacity = 0
                else:
                    attacked_squares.append((row, _col))

        # Find Available moves right
        # right means increasing column
        has_collided = False
        for _col in range(col + 1, NUM_COLS):
            if not has_collided:
                piece = app.board_helper.get_widget_at(row, _col)
                if piece.piece_type != 'blank':
                    has_collided = True
                if piece.piece_type != 'blank' and piece.player == player:
                    continue
                    #piece.indicator_opacity = 0
                else:
                    attacked_squares.append((row, _col))

        return attacked_squares, not_attacked_squares
