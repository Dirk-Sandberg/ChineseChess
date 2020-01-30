
class BoardHelper:
    @staticmethod
    def convert_to_global_indices(row, col, board_half):
        if board_half == "top":
            return row, col
        else:
            return row+5, col

    widgets_by_row_and_column = {}
    row_and_column_by_widget = {}  # Is this useful?

    def get_widget_at(self, row, column):
        return self.widgets_by_row_and_column[(row, column)]

    def get_widget_indices(self, widget):
        return self.row_and_column_by_widget[widget]

