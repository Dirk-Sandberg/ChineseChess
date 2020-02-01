from movehelper import NUM_COLS, NUM_ROWS
class BoardHelper:
    @staticmethod
    def convert_to_global_indices(row, col, board_half):
        if board_half == "top":
            return row, col
        else:
            return row+5, col

    widgets_by_row_and_column = {}
    row_and_column_by_widget = {}  # Is this useful?
    black_pieces = []
    red_pieces = []

    def get_widget_at(self, row, col):
        if row >= NUM_ROWS:
            return None
        if col >= NUM_COLS:
            return None
        if row < 0 or col < 0:
            return None
        return self.widgets_by_row_and_column[(row, col)]

    def get_widget_indices(self, player_color, piece_type):
        return self.row_and_column_by_widget["%s:%s"%(player_color,piece_type)]

