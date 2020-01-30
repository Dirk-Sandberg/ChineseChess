from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
from kivy.app import App

class ChessPiece(ButtonBehavior, Image):
    def highlight_moves(self):
        app = App.get_running_app()
        board1 = app.root.ids.game_screen.ids.top_board
        board2 = app.root.ids.game_screen.ids.top_board
        for child in board1.walk():
            if isinstance(child, Image):
                if child.source == 'dot.png':
                    child.parent.remove_widget(child)
        im1 = board1.get_widget_at(1,3)
        im = Image(source="dot.png", size=(im1.size[0]/2., im1.size[1]/2.), center=im1.center)
        im1.add_widget(im)

