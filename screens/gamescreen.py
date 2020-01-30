from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.properties import BooleanProperty


class GameScreen(Screen):
    online_mode_enabled = BooleanProperty(False)

    def highlight_available_moves(self, piece):
        pass

    def unhighlight_available_moves(self, piece):
        pass

    def start_new_game(self):
        pass

    def game_over(self):
        pass

    def remove_piece(self, piece_to_remove):
        pass

    def add_captured_piece_to_graveyard(self, captured_piece):
        pass

    def end_turn(self, player_ending_turn):
        pass
