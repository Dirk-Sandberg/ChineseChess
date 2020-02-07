from kivymd.uix.dialog import BaseGameOverDialog
from kivy.properties import NumericProperty, StringProperty#, ObjectProperty
from kivy.animation import Animation
from kivymd.uix.button import MDFloatingActionButton
from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock

class GameOverDialog(BaseGameOverDialog):
    player_elo = NumericProperty(0)
    player_nickname = StringProperty("")
    opponent_nickname = StringProperty("")
    opponent_elo = NumericProperty(0)
    change_in_elo = StringProperty("")
    text_button_ok = "Leave Game"
    text_button_cancel = "Rematch"
    is_open = False


    def __init__(self, elo1_start, elo1_stop, elo2_start, elo2_stop,
                 player_nickname, opponent_nickname, *largs, **kwargs):
        super().__init__(*largs, **kwargs)
        self.animate_elos(elo1_start, elo1_stop, elo2_start, elo2_stop)
        self.player_nickname = player_nickname
        self.opponent_nickname = opponent_nickname
        self.size_hint = (.8, .6)
        if elo1_stop > elo1_start:
            # Gained elo, make it green
            self.change_in_elo = "+%d"%(elo1_stop-elo1_start)
            self.changed_elo_label_color = [0,1,0,1]
        else:
            # Lost elo, make it red
            self.change_in_elo = "%d"%(elo1_stop-elo1_start)
            self.changed_elo_label_color = [1,0,0,1]

        # Bring up a little button that lets the user see the board
        Clock.schedule_once(self.foo, 0)

    def open(self):
        from kivy.core.window import Window
        self.pos_hint = {"center_x": .5, "center_y": .5}
        Window.add_widget(self)
        self.is_open = True


    def foo(self, *args):
        from kivy.core.window import Window
        f = MDFloatingActionButton(icon='minus', on_release=self.show_or_hide_screen)
        f.center_x = self.center_x
        f.y = self.y - f.height
        self.f = f
        f.size_hint = (None, None)
        Window.add_widget(f)

    def show_or_hide_screen(self, *args):
        if self.is_open:
            anim = Animation(pos_hint={"center_y": -self.size_hint_y/2.0, "center_x": .5})
            anim2 = Animation(y=0)
            anim.start(self)
            anim2.start(self.f)
            self.is_open = False
        else:
            fab_y = (.5-self.size_hint_y/2.0)*Window.height - self.f.height
            anim = Animation(pos_hint={"center_y": .5, "center_x": .5})
            anim2 = Animation(y=fab_y)
            anim.start(self)
            anim2.start(self.f)
            self.is_open = True

    def dismiss(self):
        anim = Animation(
            pos_hint={"center_y": -self.size_hint_y / 2.0, "center_x": .5})
        anim2 = Animation(y=-self.f.height)
        anim.start(self)
        anim2.start(self.f)
        self.is_open = False
        anim.bind(on_complete=self.back_to_lobby_browser)

    def back_to_lobby_browser(self, *args):
        app = App.get_running_app()
        app.change_screen("lobby_browser_screen")
        Window.remove_widget(self.f)
        Window.remove_widget(self)

    def animate_elos(self, elo1_start, elo1_stop, elo2_start, elo2_stop):
        self.player_elo = elo1_start
        self.opponent_elo = elo2_start
        anim = Animation(player_elo=elo1_stop, opponent_elo=elo2_stop, duration=3)
        anim.start(self)

    def request_rematch(self):
        app = App.get_running_app()
        # Ask the opponent to rematch
        message = {"command": "rematch_requested"}
        app.client.send_message(message)
        # Inform this user that they are waiting

    def leave_match(self):
        # Need to inform other player that this user left!
        print("# Need to inform other player that this user left!")
        app = App.get_running_app()
        message = {"command": "leave_match"}
        app.client.send_message(message)
        self.dismiss()

