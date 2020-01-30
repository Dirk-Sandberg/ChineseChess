"""
Meant to make it easier to index between the two grids
Easy indices to think about would be:

0,2  1,2  2,2
0,1  1,1  2,1
0,0  1,0  2,0

Without the helper, the grids go like:
0,0  0,1  0,2
1,0  1,1  1,2
2,0  2,1  2,2
 -- RIVER --
0,0  0,1  0,2
1,0  1,1  1,2
2,0  2,1  2,2

"""
from kivy.app import App


NUM_COLS = 9
NUM_ROWS = 10

def highlight_king_moves(row, col, player):
    app = App.get_running_app()
    possible_moves = [(row+1, col), (row-1, col), (row, col+1), (row, col-1)]
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
        piece = app.board_helper.get_widget_at(*move)
        if piece:
            piece.indicator_opacity = 1
            if piece.piece_type != 'blank':
                if piece.player == player:
                    piece.indicator_opacity = 0



def highlight_knight_moves(row, col, player):
    pass

def highlight_elephant_moves(row, col, player):
    app = App.get_running_app()
    possible_moves = [(row+2, col+2), (row-2, col-2), (row-2, col+2), (row+2, col-2)]
    for move in possible_moves:
        row_offset = 1 if move[0] > row else -1
        col_offset = 1 if move[1] > col else -1

        diagonal_position = (row + row_offset, col + col_offset)
        piece = app.board_helper.get_widget_at(*diagonal_position)
        if piece:
            if piece.piece_type != 'blank':
                # There is a piece blocking the elephant's path
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
            piece.indicator_opacity = 1
            if piece.piece_type != 'blank':
                if piece.player == player:
                    piece.indicator_opacity = 0



def highlight_guard_moves(row, col, player):
    app = App.get_running_app()
    possible_moves = [(row+1, col+1), (row-1, col-1), (row-1, col+1), (row+1, col-1)]
    for move in possible_moves:
        # Make sure the move is inside the palace
        if move[1] > 5:
            # Trying to move to the right of the palace
            continue
        if move[1] < 3:
            # Trying to move to the left of the palace
            continue
        if move[0] < 7 and player == 'red':
            continue
        if move[0] > 2 and player == 'black':
            continue

        piece = app.board_helper.get_widget_at(*move)
        if piece:
            piece.indicator_opacity = 1
            if piece.piece_type != 'blank':
                if piece.player == player:
                    piece.indicator_opacity = 0


def highlight_cannon_moves(row, col, player):
    pass

def highlight_pawn_moves(row, col, player):
    app = App.get_running_app()
    if player == 'black':
        # Pawn can move down but not up
        if row != NUM_ROWS-1:
            piece = app.board_helper.get_widget_at(row+1, col)
            piece.indicator_opacity = 1
            if piece.piece_type != 'blank':
                if piece.player == player:
                    piece.indicator_opacity = 0

        # If pawn is past river, can move left and right
        if row > 4:
            piece = app.board_helper.get_widget_at(row, col-1)
            if piece:
                piece.indicator_opacity = 1
                if piece.piece_type != 'blank':
                    if piece.player == player:
                        piece.indicator_opacity = 0
            piece = app.board_helper.get_widget_at(row, col+1)
            if piece:
                piece.indicator_opacity = 1
                if piece.piece_type != 'blank':
                    if piece.player == player:
                        piece.indicator_opacity = 0


    else:
        # Pawn can move up but not down
        if row != 0:
            piece = app.board_helper.get_widget_at(row-1, col)
            piece.indicator_opacity = 1
            if piece.piece_type != 'blank':
                if piece.player == player:
                    piece.indicator_opacity = 0


        # If pawn is past river, can move left and right
        if row < 5:
            piece = app.board_helper.get_widget_at(row, col-1)
            if piece:
                piece.indicator_opacity = 1
                if piece.piece_type != 'blank':
                    if piece.player == player:
                        piece.indicator_opacity = 0

            piece = app.board_helper.get_widget_at(row, col+1)
            if piece:
                piece.indicator_opacity = 1
                if piece.piece_type != 'blank':
                    if piece.player == player:
                        piece.indicator_opacity = 0


def highlight_rook_moves(row, col, player):
    app = App.get_running_app()
    # Find Available moves down
    # down means increasing row
    has_collided = False
    for _row in range(row+1, NUM_ROWS):
        if not has_collided:
            piece = app.board_helper.get_widget_at(_row, col)
            piece.indicator_opacity = 1
            if piece.piece_type != 'blank':
                has_collided = True
                if piece.player == player:
                    piece.indicator_opacity = 0

    # Find Available moves up
    # up means decreasing row
    has_collided = False
    for _row in range(0, row)[::-1]:
        if not has_collided:
            piece = app.board_helper.get_widget_at(_row, col)
            piece.indicator_opacity = 1
            if piece.piece_type != 'blank':
                has_collided = True
                if piece.player == player:
                    piece.indicator_opacity = 0

    # Find Available moves left
    # left means decreasing column
    has_collided = False
    for _col in range(0, col)[::-1]:
        if not has_collided:
            piece = app.board_helper.get_widget_at(row, _col)
            piece.indicator_opacity = 1
            if piece.piece_type != 'blank':
                has_collided = True
                if piece.player == player:
                    piece.indicator_opacity = 0

    # Find Available moves right
    # right means increasing column
    has_collided = False
    for _col in range(col+1, NUM_COLS):
        if not has_collided:
            piece = app.board_helper.get_widget_at(row, _col)
            piece.indicator_opacity = 1
            if piece.piece_type != 'blank':
                has_collided = True
                if piece.player == player:
                    piece.indicator_opacity = 0



