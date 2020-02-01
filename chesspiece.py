from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.app import App
from kivy.properties import OptionProperty, StringProperty

from availablemoveindicator import AvailableMoveIndicator
from kivy.core.window import Window

class ChessPiece(ButtonBehavior, Image):
    piece_type = OptionProperty("blank", options=["blank", "rook", "cannon","pawn", "king", "knight", "guard", "elephant"])
    player = StringProperty("black")

    def id(self):
        return "%s %s at (%s, %s)"%(self.player, self.piece_type, self.row, self.col)

    def move_piece(self):
        app = App.get_running_app()

        # Animate the motion
        animation_widget = Image(source=app.highlighted_piece.source,
                                 color=app.highlighted_piece.color,
                                 keep_ratio=False, allow_stretch=True)
        animation_widget.size_hint = (None, None)
        animation_widget.size = app.highlighted_piece.size
        animation_widget.pos = self.to_window(*app.highlighted_piece.pos)
        Window.add_widget(animation_widget)
        new_pos = self.to_window(*self.pos)
        app.highlighted_piece.opacity = 0
        app.is_animating = True
        anim = Animation(pos=new_pos)
        anim.bind(on_complete=self.finish_piece_movement)
        anim.start(animation_widget)

    def finish_piece_movement(self, animation, animated_object):
        app = App.get_running_app()
        app.highlighted_piece.opacity = 1

        black_captured_pieces_grid = app.root.ids.game_screen.ids.captured_black_pieces
        red_captured_pieces_grid = app.root.ids.game_screen.ids.captured_red_pieces
        if self.piece_type != 'blank':
            if self.player == 'black':
                red_captured_pieces_grid.add_widget(
                    Image(source=self.source, color=self.color))
            else:
                black_captured_pieces_grid.add_widget(
                    Image(source=self.source, color=self.color))



        # Place a blank piece in place of the one that just moved
        app.root.ids.game_screen.move_pieces(self, app.highlighted_piece)


        # Remove the captured piece from the list of black/red pieces
        # Only works if the piece hasn't moved because i'm not actually moving
        # chess pieces around, im just changing the image of the board
        widget_to_remove = self
        if widget_to_remove in app.board_helper.black_pieces:
            app.board_helper.black_pieces.remove(widget_to_remove)
            print("Removing me", widget_to_remove.player, widget_to_remove.piece_type)
        if widget_to_remove in app.board_helper.red_pieces:
            app.board_helper.red_pieces.remove(widget_to_remove)
            print("Removing me", widget_to_remove.player, widget_to_remove.piece_type)


        animated_object.parent.remove_widget(animated_object)
        # The piece has been captured if it wasn't blank!
        app.is_animating = False


    def handle_touch(self):
        app = App.get_running_app()
        #print("Touched", self.id())
        if app.is_animating:
            return
        if self.indicator_opacity == 1:
            # Game needs to move the highlighted widget
            self.move_piece()
            self.clear_indicators()
        else:
            self.clear_indicators()
            self.highlight_moves()

    def highlight_moves(self):
        print("%s doesn't account for flying king yet"%self.piece_type)
        app = App.get_running_app()
        app.highlighted_piece = self
        attacked, not_attacked = self.get_attacked_squares()
        for square in attacked:
            self.highlight_legal_move(square)
        for square in not_attacked:
            self.highlight_illegal_move(square)

    def get_attacked_squares(self):
        """
        TO BE OVERRIDDEN BY SUBCLASSED PIECES
        :return:
        """
        return [], []

    def highlight_legal_move(self, square):
        app = App.get_running_app()
        app.root.ids.game_screen.check_for_check()
        piece = app.board_helper.get_widget_at(square[0], square[1])
        if piece:
            piece.indicator_opacity = 1

    def highlight_illegal_move(self, square):
        app = App.get_running_app()
        piece = app.board_helper.get_widget_at(square[0], square[1])
        if piece:
            piece.indicator_opacity = .5


    def clear_indicators(self):
        app = App.get_running_app()
        board1 = app.root.ids.game_screen.ids.top_board
        board2 = app.root.ids.game_screen.ids.bottom_board
        # Clear all indicators
        for child in board1.walk():
            child.indicator_opacity = 0
        for child in board2.walk():
            child.indicator_opacity = 0


