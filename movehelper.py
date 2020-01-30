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
    for _row in range(0, row):
        if not has_collided:
            piece = app.board_helper.get_widget_at(_row, col)
            piece.indicator_opacity = 1
            if piece.piece_type != 'blank':
                has_collided = True
            if piece.player == player:
                piece.indicator_opacity = 0

    # Find Available moves right
    # right means increasing column


    #HIGHLIGHT EVERYTHING
    #for _col in range(NUM_COLS):
    #    widget = app.board_helper.get_widget_at(row, _col)
    #    widget.indicator_opacity = 1
    #for _row in range(NUM_ROWS):
    #    widget = app.board_helper.get_widget_at(_row, col)
    #    widget.indicator_opacity = 1


def get_piece_from_global_index(local_col, local_row, half):
    pass

