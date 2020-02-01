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

    def highlight_king_moves(self, row, col, player):
        print("King doesn't properly account for flying king yet")
        attacked, not_attacked = get_attacked_king_squares(row, col, player)
        for square in attacked:
            highlight_legal_move(square)
        for square in not_attacked:
            highlight_illegal_move(square)

    def get_attacked_king_squares(self, row, col, player):
        app = App.get_running_app()
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

    def highlight_knight_moves(self, row, col, player):
        print("knight doesn't account for flying king yet")
        attacked, not_attacked = self.get_attacked_knight_squares(row, col, player)
        for square in attacked:
            self.highlight_legal_move(square)
        for square in not_attacked:
            self.highlight_illegal_move(square)

    def get_attacked_knight_squares(self, row, col, player):
        app = App.get_running_app()
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

    def highlight_elephant_moves(self, row, col, player):
        print("elephant doesn't account for flying king yet")
        attacked, not_attacked = self.get_attacked_elephant_squares(row, col, player)
        for square in attacked:
            self.highlight_legal_move(square)
        for square in not_attacked:
            self.highlight_illegal_move(square)

    def get_attacked_elephant_squares(self, row, col, player):
        app = App.get_running_app()
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
            if move[0] < 5 and player == 'red':
                # Trying to move up from river
                continue
            if move[0] > 4 and player == 'black':
                # Trying to move down from river
                continue

            piece = app.board_helper.get_widget_at(*move)
            if piece:
                if piece.piece_type != 'blank' and piece.player == player:
                    pass
                else:
                    attacked_squares.append(move)
        return attacked_squares, not_attacked_squares

    def highlight_guard_moves(self, row, col, player):
        print("guard doesn't account for flying king yet")
        attacked, not_attacked = self.get_attacked_guard_squares(row, col, player)
        for square in attacked:
            self.highlight_legal_move(square)
        for square in not_attacked:
            self.highlight_illegal_move(square)

    def get_attacked_guard_squares(self, row, col, player):
        app = App.get_running_app()
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
            if move[0] < 7 and player == 'red':
                # Trying to move above palace
                continue
            if move[0] > 2 and player == 'black':
                # Trying to move below palace
                continue

            piece = app.board_helper.get_widget_at(*move)
            if piece:
                if piece.piece_type != 'blank' and piece.player == player:
                    pass
                else:
                    attacked_squares.append(move)

        return attacked_squares, not_attacked_squares

    def highlight_cannon_moves(self, row, col, player):
        print("Cannon doesn't account for flying king yet")
        attacked, not_attacked = self.get_attacked_cannon_squares(row, col, player)
        for square in attacked:
            self.highlight_legal_move(square)
        for square in not_attacked:
            self.highlight_illegal_move(square)

    def get_attacked_cannon_squares(self, row, col, player):
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
                    attacked_squares.append([_row, col])
                else:
                    # piece.indicator_opacity = 0
                    collides += 1
            elif collides == 1:
                if piece.piece_type != 'blank':
                    collides += 1
                    if piece.player != player:
                        attacked_squares.append([_row, col])

        # Find Available moves up
        # up means decreasing row
        collides = 0
        for _row in range(0, row)[::-1]:
            piece = app.board_helper.get_widget_at(_row, col)
            if collides == 0:
                if piece.piece_type == 'blank':
                    attacked_squares.append([_row, col])
                else:
                    # piece.indicator_opacity = 0
                    collides += 1
            elif collides == 1:
                if piece.piece_type != 'blank':
                    collides += 1
                    if piece.player != player:
                        attacked_squares.append([_row, col])

        # Find Available moves left
        # left means decreasing column
        collides = 0
        for _col in range(0, col)[::-1]:
            piece = app.board_helper.get_widget_at(row, _col)
            if collides == 0:
                if piece.piece_type == 'blank':
                    attacked_squares.append([row, _col])
                else:
                    # piece.indicator_opacity = 0
                    collides += 1
            elif collides == 1:
                if piece.piece_type != 'blank':
                    collides += 1
                    if piece.player != player:
                        attacked_squares.append([row, _col])

        # Find Available moves right
        # right means increasing column
        collides = 0
        for _col in range(col + 1, NUM_COLS):
            piece = app.board_helper.get_widget_at(row, _col)
            if collides == 0:
                if piece.piece_type == 'blank':
                    attacked_squares.append([row, _col])
                else:
                    # piece.indicator_opacity = 0
                    collides += 1
            elif collides == 1:
                if piece.piece_type != 'blank':
                    collides += 1
                    if piece.player != player:
                        attacked_squares.append([row, _col])
        return attacked_squares, not_attacked_squares

    def highlight_pawn_moves(row, col, player):
        print("Pawn doesn't account for flying king yet")
        attacked, not_attacked = get_attacked_pawn_squares(row, col, player)
        for square in attacked:
            highlight_legal_move(square)
        for square in not_attacked:
            highlight_illegal_move(square)

    def get_attacked_pawn_squares(self, row, col, player):
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
                    attacked_squares.append([row + 1, col])

            # If pawn is past river, can move left and right
            if row > 4:
                piece = app.board_helper.get_widget_at(row, col - 1)
                if piece:
                    if piece.piece_type != 'blank' and piece.player == player:
                        piece.indicator_opacity = 0
                    else:
                        attacked_squares.append([row, col - 1])
                piece = app.board_helper.get_widget_at(row, col + 1)
                if piece:
                    if piece.piece_type != 'blank' and piece.player == player:
                        piece.indicator_opacity = 0
                    else:
                        attacked_squares.append([row, col + 1])


        else:
            # Pawn can move up but not down
            if row != 0:
                piece = app.board_helper.get_widget_at(row - 1, col)
                if piece.piece_type != 'blank' and piece.player == player:
                    piece.indicator_opacity = 0
                else:
                    attacked_squares.append([row - 1, col])

            # If pawn is past river, can move left and right
            if row < 5:
                piece = app.board_helper.get_widget_at(row, col - 1)
                if piece:
                    if piece.piece_type != 'blank' and piece.player == player:
                        piece.indicator_opacity = 0
                    else:
                        attacked_squares.append([row, col - 1])

                piece = app.board_helper.get_widget_at(row, col + 1)
                if piece:
                    if piece.piece_type != 'blank' and piece.player == player:
                        piece.indicator_opacity = 0
                    else:
                        attacked_squares.append([row, col + 1])
        return attacked_squares, not_attacked_squares


