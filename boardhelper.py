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

    def get_widget_at(self, row, col):
        if row >= NUM_ROWS:
            return None
        if col >= NUM_COLS:
            return None
        if row < 0 or col < 0:
            return None
        return self.widgets_by_row_and_column[(row, col)]

    def get_widget_indices(self, widget):
        return self.row_and_column_by_widget[widget]

