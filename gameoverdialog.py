from kivymd.uix.dialog import MDDialog
from kivy.properties import NumericProperty
from kivy.animation import Animation
from kivy.event import EventDispatcher
from kivy.clock import mainthread

class GameOverDialog(MDDialog, EventDispatcher):
    player_elo = NumericProperty(0)
    opponent_elo = NumericProperty(0)
    text_button_ok = "Leave Game"
    text_button_cancel = "Rematch"

    def __init__(self, elo1_start, elo1_stop, elo2_start, elo2_stop, *largs, **kwargs):
        super().__init__(*largs, **kwargs)
        self.animate_elos(elo1_start, elo1_stop, elo2_start, elo2_stop)

    def animate_elos(self, elo1_start, elo1_stop, elo2_start, elo2_stop):
        self.player_elo = elo1_start
        self.opponent_elo = elo2_start
        anim = Animation(player_elo=elo1_stop, opponent_elo=elo2_stop, duration=4)
        anim.start(self)

    def events_callback(self, text_of_selection, dialog):
        if text_of_selection == 'Rematch':
            print("Rematch")
        elif text_of_selection == "Leave Game":
            print("Leave Game")

