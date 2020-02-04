from chesspieces.chesspiece import ChessPiece
from kivy.app import App
from movehelper import NUM_ROWS


class KingPiece(ChessPiece):
    piece_type = "king"

    def get_attacked_squares(self):
        app = App.get_running_app()
        row, col, player = self.row, self.col, self.player
        king_is_this_players = True if player == 'red' and app.player.is_red or player == 'black' and not app.player.is_red else False
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
            if move[0] < 7 and king_is_this_players:# player == 'red':
                # Trying to move up from palace
                continue
            if move[0] > 2 and not king_is_this_players:#player == 'black':
                # Trying to move up from palace
                continue


            # Check for the flying king rule
            # Get column for both kings
            # If the column from move[1] is the same as the enemy_king.col
                # if no other units in that column with row between king cols
                    # Rule violated
            # Get all pieces in the column that the king is trying to move to
            pieces_in_same_column = []
            for _row in range(NUM_ROWS):
                piece = app.board_helper.get_widget_at(_row, move[1])
                if piece.piece_type != 'blank':
                    pieces_in_same_column.append(piece)
            enemy_color = 'red' if player == 'black' else 'black'
            enemy_king = app.board_helper.get_widget_by_color_and_type(enemy_color, 'king')
            if move[1] == enemy_king.col:
                # King is moving to same column as enemy king
                min_row = min([self.row, enemy_king.row])
                max_row = max([self.row, enemy_king.row])
                piece_is_between_kings = False
                # See if any pieces are between the two kings
                for piece in pieces_in_same_column:
                    if piece.row < max_row and piece.row > min_row:
                        piece_is_between_kings = True
                # If there was no piece blocking the kings, rule violated
                if not piece_is_between_kings:
                    # Flying king rule was violated. Don't let the king go there
                    not_attacked_squares.append(move)
                    # Go to the next move
                    continue

            piece = app.board_helper.get_widget_at(*move)
            if piece:
                if piece.piece_type != 'blank' and piece.player == player:
                    pass
                else:
                    attacked_squares.append(move)


        # Add an attacked move for the flying king rule
        # Get all pieces in the column that the king is trying to move to
        pieces_in_same_column = []
        for _row in range(NUM_ROWS):
            piece = app.board_helper.get_widget_at(_row, self.col)
            if piece.piece_type != 'blank':
                pieces_in_same_column.append(piece)
        enemy_color = 'red' if player == 'black' else 'black'
        enemy_king = app.board_helper.get_widget_by_color_and_type(enemy_color, 'king')
        if self.col == enemy_king.col:
            # King is moving to same column as enemy king
            min_row = min([self.row, enemy_king.row])
            max_row = max([self.row, enemy_king.row])
            piece_is_between_kings = False
            # See if any pieces are between the two kings
            for piece in pieces_in_same_column:
                if piece.row < max_row and piece.row > min_row:
                    piece_is_between_kings = True
            # If there was no piece blocking the kings, rule violated
            if not piece_is_between_kings:
                # King could theoretically attack the other king
                attacked_squares.append((enemy_king.row, enemy_king.col))

        return attacked_squares, not_attacked_squares
