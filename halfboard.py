from kivy.uix.gridlayout import GridLayout
from kivy.properties import NumericProperty
from chesspiece import ChessPiece
from kivy.uix.widget import Widget
from kivy.core.window import Window


class HalfBoard(GridLayout):
    rows = NumericProperty(5)
    cols = NumericProperty(9)
    widgets_by_row_and_column = {}

    def get_widget_at(self, row, column):
        return self.widgets_by_row_and_column[(row, column)]

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        for row in range(self.rows):
            for col in range(self.cols):
                c = ChessPiece()#source="redpiece.png")
                self.add_widget(c)
                self.widgets_by_row_and_column[(row, col)] = c

