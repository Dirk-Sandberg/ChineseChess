from chesspiece import ChessPiece
from kivy.app import App
from movehelper import NUM_COLS, NUM_ROWS


class CannonPiece(ChessPiece):
    piece_type = "cannon"

    def get_attacked_squares(self):
        row, col, player = self.row, self.col, self.player
        attacked_squares = []
        not_attacked_squares = []  # From being blocked or flying king rule
        app = App.get_running_app()
        # Find Available moves down
        # down means increasing row
        collides = 0
        for _row in range(row + 1, NUM_ROWS):
            piece = app.board_helper.get_widget_at(_row, col)
            if collides == 0:
                if piece.piece_type == 'blank':
                    attacked_squares.append((_row, col))
                else:
                    piece.indicator_opacity = 0
                    collides += 1
            elif collides == 1:
                if piece.piece_type != 'blank':
                    collides += 1
                    if piece.player != player:
                        attacked_squares.append((_row, col))

        # Find Available moves up
        # up means decreasing row
        collides = 0
        for _row in range(0, row)[::-1]:
            piece = app.board_helper.get_widget_at(_row, col)
            if collides == 0:
                if piece.piece_type == 'blank':
                    attacked_squares.append((_row, col))
                else:
                    piece.indicator_opacity = 0
                    collides += 1
            elif collides == 1:
                if piece.piece_type != 'blank':
                    collides += 1
                    if piece.player != player:
                        attacked_squares.append((_row, col))

        # Find Available moves left
        # left means decreasing column
        collides = 0
        for _col in range(0, col)[::-1]:
            piece = app.board_helper.get_widget_at(row, _col)
            if collides == 0:
                if piece.piece_type == 'blank':
                    attacked_squares.append((row, _col))
                else:
                    piece.indicator_opacity = 0
                    collides += 1
            elif collides == 1:
                if piece.piece_type != 'blank':
                    collides += 1
                    if piece.player != player:
                        attacked_squares.append((row, _col))

        # Find Available moves right
        # right means increasing column
        collides = 0
        for _col in range(col + 1, NUM_COLS):
            piece = app.board_helper.get_widget_at(row, _col)
            if collides == 0:
                if piece.piece_type == 'blank':
                    attacked_squares.append((row, _col))
                else:
                    piece.indicator_opacity = 0
                    collides += 1
            elif collides == 1:
                if piece.piece_type != 'blank':
                    collides += 1
                    if piece.player != player:
                        attacked_squares.append((row, _col))
        return attacked_squares, not_attacked_squares
