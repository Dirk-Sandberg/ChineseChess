from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.app import App
from kivy.properties import OptionProperty, StringProperty
from movehelper import highlight_rook_moves, highlight_pawn_moves, \
    highlight_king_moves, highlight_guard_moves, highlight_elephant_moves, \
    highlight_cannon_moves, highlight_knight_moves

from availablemoveindicator import AvailableMoveIndicator
from kivy.core.window import Window

class ChessPiece(ButtonBehavior, Image):
    piece_type = OptionProperty("pawn", options=["blank", "rook", "cannon","pawn", "king", "knight", "guard", "elephant"])
    player = StringProperty("black")

    def move_piece(self):
        app = App.get_running_app()

        # Animate the motion
        animation_widget = Image(source=app.highlighted_piece.source,
                                 color = app.highlighted_piece.color,
                                 keep_ratio=False,allow_stretch=True)
        animation_widget.size_hint = (None, None)
        animation_widget.size = app.highlighted_piece.size
        animation_widget.pos = self.to_window(*app.highlighted_piece.pos)
        Window.add_widget(animation_widget)
        new_pos = self.to_window(*self.pos)
        app.highlighted_piece.source = 'images/blankpiece.png'
        app.is_animating = True
        anim = Animation(pos=new_pos)
        anim.bind(on_complete=self.finish_piece_movement)
        anim.start(animation_widget)

    def finish_piece_movement(self, animation, animated_object):
        app = App.get_running_app()

        black_captured_pieces_grid = app.root.ids.game_screen.ids.captured_black_pieces
        red_captured_pieces_grid = app.root.ids.game_screen.ids.captured_red_pieces
        if self.piece_type != 'blank':
            if self.player == 'black':
                red_captured_pieces_grid.add_widget(
                    Image(source=self.source, color=self.color))
            else:
                black_captured_pieces_grid.add_widget(
                    Image(source=self.source, color=self.color))

        animated_object.parent.remove_widget(animated_object)
        # The piece has been captured if it wasn't blank!
        self.piece_type = app.highlighted_piece.piece_type
        self.player = app.highlighted_piece.player
        app.highlighted_piece.piece_type = 'blank'
        app.is_animating = False

    def highlight_moves(self):
        app = App.get_running_app()
        if app.is_animating:
            return
        board1 = app.root.ids.game_screen.ids.top_board
        board2 = app.root.ids.game_screen.ids.bottom_board

        # If they clicked on a highlighted spot, move their piece
        if self.indicator_opacity == 1:
            self.move_piece()
            # Clear all indicators
            for child in board1.walk():
                child.indicator_opacity = 0
            for child in board2.walk():
                child.indicator_opacity = 0
            return
        else:
            app.highlighted_piece = self
        # Clear all indicators
        for child in board1.walk():
            child.indicator_opacity = 0
        for child in board2.walk():
            child.indicator_opacity = 0

        if self.piece_type == "rook":
            highlight_rook_moves(self.row, self.col, self.player)
        if self.piece_type == "pawn":
            highlight_pawn_moves(self.row, self.col, self.player)
        if self.piece_type == 'guard':
            highlight_guard_moves(self.row, self.col, self.player)
        if self.piece_type == 'king':
            highlight_king_moves(self.row, self.col, self.player)
        if self.piece_type == 'elephant':
            highlight_elephant_moves(self.row, self.col, self.player)
        if self.piece_type == 'cannon':
            highlight_cannon_moves(self.row, self.col, self.player)
        if self.piece_type == 'knight':
            highlight_knight_moves(self.row, self.col, self.player)

