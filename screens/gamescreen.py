from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.properties import BooleanProperty, ObjectProperty
from chesspieces.chesspiece import ChessPiece
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.clock import mainthread
from functools import partial
from kivymd.uix.dialog import MDDialog
from gameoverdialog import GameOverDialog


class GameScreen(Screen):
    online_mode_enabled = BooleanProperty(False)
    game_over_dialog = ObjectProperty(None)

    def return_to_home_screen(self):
        self.manager.current = 'home_screen'

    @mainthread
    def new_game(self):
        board_helper = App.get_running_app().board_helper
        board_helper.widgets_by_row_and_column = {}
        board_helper.widgets_by_color_and_type = {}
        board_helper.black_pieces = []
        board_helper.red_pieces = []

        self.ids.top_captured_pieces.clear_widgets()
        self.ids.bottom_captured_pieces.clear_widgets()

        top_board = self.ids.top_board
        bottom_board = self.ids.bottom_board
        top_board.clear_widgets()
        bottom_board.clear_widgets()
        top_board.add_starting_pieces()
        bottom_board.add_starting_pieces()


    def mirror_col(self, col):
        # Find distance from center
        return int(4 - (col-4))

    def mirror_row(self, row):
        return int(4.5 - (row-4.5))

    @mainthread
    def move_piece(self, from_row, from_col, to_row, to_col, moved_piece_color):
        """
        To be called when the client receives a "piece_moved" command
        :return:
        """
        app = App.get_running_app()
        # Clear the image that showed where the last piece moved from
        self.clear_just_moved_indicator()

        # Need to mirror the rows and columns if the player isn't the client
        if moved_piece_color == "red" and app.player.is_red or moved_piece_color == 'black' and not app.player.is_red:
            pass
        else:
            # Mirror the movements
            from_row = self.mirror_row(from_row)
            from_col = self.mirror_col(from_col)
            to_row = self.mirror_row(to_row)
            to_col = self.mirror_col(to_col)

        # Get the widget being moved
        moving_piece = app.board_helper.get_widget_at(from_row, from_col)
        piece_being_entered = app.board_helper.get_widget_at(to_row, to_col)
        #print("Moving piece", moving_piece.id())



        # Animate the motion
        animation_widget = Image(source=moving_piece.source,
                                 color=moving_piece.color,
                                 keep_ratio=False, allow_stretch=True)
        animation_widget.size_hint = (None, None)
        animation_widget.size = moving_piece.size
        animation_widget.pos = self.to_window(*moving_piece.pos)
        Window.add_widget(animation_widget)
        new_pos = piece_being_entered.pos
        moving_piece.opacity = 0
        app.is_animating = True
        anim = Animation(pos=new_pos)#, duration=0)
        anim.bind(on_complete=partial(self.finish_piece_movement, piece_being_entered, moving_piece))
        anim.start(animation_widget)

    def finish_piece_movement(self, piece_being_entered, moving_piece, animation, animated_object):
        app = App.get_running_app()
        moving_piece.opacity = 1

        #black_captured_pieces_grid = app.root.ids.game_screen.ids.captured_black_pieces
        #red_captured_pieces_grid = app.root.ids.game_screen.ids.captured_red_pieces
        top_captured_pieces_grid = app.root.ids.game_screen.ids.top_captured_pieces
        bottom_captured_pieces_grid = app.root.ids.game_screen.ids.bottom_captured_pieces

        if piece_being_entered.piece_type != 'blank':
            if piece_being_entered.player == 'black' and app.player.is_red or piece_being_entered.player == 'red' and not app.player.is_red:
                bottom_captured_pieces_grid.add_widget(
                    Image(source=piece_being_entered.source, color=piece_being_entered.color))
            else:
                top_captured_pieces_grid.add_widget(
                    Image(source=piece_being_entered.source, color=piece_being_entered.color))



        # Place a blank piece in place of the one that just moved
        self.move_pieces(piece_being_entered, moving_piece)


        # Remove the captured piece from the list of black/red pieces
        # Only works if the piece hasn't moved because i'm not actually moving
        # chess pieces around, im just changing the image of the board
        widget_to_remove = piece_being_entered
        if widget_to_remove in app.board_helper.black_pieces:
            app.board_helper.black_pieces.remove(widget_to_remove)
            #print("Removing me", widget_to_remove.player, widget_to_remove.piece_type)
        if widget_to_remove in app.board_helper.red_pieces:
            app.board_helper.red_pieces.remove(widget_to_remove)
            #print("Removing me", widget_to_remove.player, widget_to_remove.piece_type)


        animated_object.parent.remove_widget(animated_object)
        # The piece has been captured if it wasn't blank!
        app.is_animating = False

        # Check if this move put the enemy's king in check
        enemy_is_in_check = self.check_for_check(moving_piece.player, simulated_move=False)
        if enemy_is_in_check:
            enemy_color = 'red' if moving_piece.player == 'black' else 'black'
            CHECKMATE = self.check_for_checkmate(enemy_color)
            if CHECKMATE:
                app.checkmate(enemy_color)
            else:
                m = MDDialog(title="Check", text=enemy_color + " is in check")
                m.open()

        # Stop highlighting the piece
        moving_piece.indicator_source = "moved_from"
        app.highlighted_piece = None



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
        new_blank_piece.indicator_source = "moved_from"
        from_parent.add_widget(new_blank_piece, moving_from)
        piece_moving.row = piece_being_entered_upon.row
        piece_moving.col = piece_being_entered_upon.col

        # Update the references to widgets by their col and row in board helper
        app = App.get_running_app()
        board = app.board_helper
        board.widgets_by_row_and_column[(piece_moving.row, piece_moving.col)] = piece_moving
        board.widgets_by_row_and_column[(new_blank_piece.row, new_blank_piece.col)] = new_blank_piece


    def check_for_check(self, player, simulated_move):
        """

        :param player: The color of the moving piece
        :param simulated_move: If True, will see if moving the piece puts his
        own king in check. If False, will see if moving the piece has put the
        enemy's king in check.
        :return:
        """
        app = App.get_running_app()
        black_pieces = app.board_helper.black_pieces
        red_pieces = app.board_helper.red_pieces
        # IF SIMULATED MOVE, check if the move makes my OWN king in check
        # (check for check called BEFORE this player moves -- to find invalid moves)
        if player == 'red' and simulated_move or not player == 'red' and not simulated_move:
            attacked_player = 'red'
            pieces = black_pieces
        else:
            # elif app.player.is_red and not simulated_move or not app.player.is_red and simulated_move:
            # IF NOT SIMULATED MOVE, check if the move makes ENEMY king in check
            # (check for check called after this player made a move)
            attacked_player = 'black'
            pieces = red_pieces

        attacked_king = app.board_helper.get_widget_by_color_and_type(attacked_player, 'king')
        attacked_king = (attacked_king.row, attacked_king.col)
        for piece in pieces:
            attacked_squares, not_attacked_squares = piece.get_attacked_squares()
            if attacked_king in attacked_squares:
                #if not simulated_move:
                #    print(attacked_player + " KING IS ATTACKED by", piece.id())
                #if simulated_move:
                #    print("SIMULATION: " + player + " KING IS ATTACKED by", piece.id())
                return True
        return False

    def check_for_checkmate(self, color_in_check):
        app = App.get_running_app()
        if color_in_check == 'black':
            # Try to move all black pieces
            # If all moves are illegal, game ends
            black_pieces = app.board_helper.black_pieces
            for piece in black_pieces:
                legal_moves, illegal_moves = piece.get_moves()
                if legal_moves != []:
                    # Black can make a move. not checkmate
                    return False
        else:
            # Try to move all red pieces
            # If all moves are illegal, game ends
            red_pieces = app.board_helper.red_pieces
            for piece in red_pieces:
                legal_moves, illegal_moves = piece.get_moves()
                if legal_moves != []:
                    # red can make a move. not checkmate
                    return False

        return True


    def simulate_board_with_changed_piece_position(self,piece,new_row,new_col):
        app = App.get_running_app()
        # Get references to previous game state
        board = app.board_helper
        old_row, old_col = piece.row, piece.col
        old_widgets_by_row_and_column = board.widgets_by_row_and_column.copy()
        old_black_pieces = app.board_helper.black_pieces.copy()
        old_red_pieces = app.board_helper.red_pieces.copy()

        # Simulate new game state and look for check
        # Put a blank piece in the spot where the moving piece came from
        board.widgets_by_row_and_column[(piece.row, piece.col)] = ChessPiece(col=piece.col,row=piece.row)
        piece.row = new_row
        piece.col = new_col

        # If the square being moved onto was owned by a piece, remove it from
        # the list of black or red pieces respectively
        piece_being_entered = board.widgets_by_row_and_column[(new_row, new_col)]
        widget_to_remove = piece_being_entered
        if widget_to_remove in app.board_helper.black_pieces:
            app.board_helper.black_pieces.remove(widget_to_remove)
        if widget_to_remove in app.board_helper.red_pieces:
            app.board_helper.red_pieces.remove(widget_to_remove)

        board.widgets_by_row_and_column[(new_row, new_col)] = piece
        check_is_in_simulated_game_state = self.check_for_check(piece.player, simulated_move=True)

        # Change game state back to original state
        piece.row = old_row
        piece.col = old_col
        board.widgets_by_row_and_column = old_widgets_by_row_and_column
        app.board_helper.black_pieces = old_black_pieces
        app.board_helper.red_pieces = old_red_pieces

        return check_is_in_simulated_game_state

    def clear_just_moved_indicator(self):
        board1 = self.ids.top_board
        board2 = self.ids.bottom_board
        # Clear all indicators that don't show where a piece just moved from
        for child in board1.children:
            if child.indicator_source == "moved_from":
                child.indicator_source = "blankpiece"
        for child in board2.children:
            if child.indicator_source == "moved_from":
                child.indicator_source = "blankpiece"

    def forfeit(self):
        # Send a message to the server that this player forfeited
        app = App.get_running_app()
        loser_color = 'red' if app.player.is_red else 'black'
        message = {"command": "forfeit", "loser_color": loser_color}
        app.client.send_message(message)

    def rematch_request_revoked(self):
        self.game_over_dialog.ids.opponent_is_ready_checkbox.active = False

    def rematch_requested(self):
        self.game_over_dialog.ids.opponent_is_ready_checkbox.active = True
        if self.game_over_dialog.ids.player_is_ready_checkbox.active:
            # Both players are active, start the game
            self.accept_rematch()

    def accept_rematch(self):
        app = App.get_running_app()
        message = {"command": "rematch_accepted"}
        app.client.send_message(message)
        self.game_over_dialog.dismiss()

    def display_game_over_dialog(self, winner_color, loser_elo, new_loser_elo, winner_elo,
                                 new_winner_elo, nickname, opponent_nickname):
        self.game_over_dialog = GameOverDialog(winner_color, loser_elo, new_loser_elo,
                                               winner_elo, new_winner_elo,
                                               nickname, opponent_nickname)
        self.game_over_dialog.open()





