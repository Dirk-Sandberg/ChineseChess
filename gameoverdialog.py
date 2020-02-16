from kivymd.uix.dialog import BaseGameOverDialog
from kivy.properties import NumericProperty, StringProperty#, ObjectProperty
from kivy.animation import Animation
from gameoverfab import GameOverFab
from kivy.app import App
from kivy.core.window import Window


class GameOverDialog(BaseGameOverDialog):
    player_elo = NumericProperty(0)
    player_nickname = StringProperty("")
    opponent_nickname = StringProperty("")
    opponent_elo = NumericProperty(0)
    change_in_elo = StringProperty("")
    text_button_ok = "Leave Game"
    text_button_cancel = "Rematch"
    fab = None
    is_open = False


    def __init__(self, winner_color, loser_elo, new_loser_elo,
                                               winner_elo, new_winner_elo,
                 player_nickname, opponent_nickname, *largs, **kwargs):
        super().__init__(*largs, **kwargs)
        app = App.get_running_app()
        self.title = winner_color[0].upper() + winner_color[1:] + " Wins!"
        if winner_color == 'red' and app.player.is_red or winner_color == 'black' and not app.player.is_red:
            elo_start = winner_elo
            elo_stop = new_winner_elo
        else:
            elo_start = loser_elo
            elo_stop = new_loser_elo
        self.animate_elos(elo_start, elo_stop)
        self.player_nickname = player_nickname
        self.opponent_nickname = opponent_nickname
        self.size_hint = (.8, .6)
        self.pos_hint = {"center_y": -self.size_hint_y, "center_x": .5}
        if elo_stop > elo_start:
            # Gained elo, make it green
            self.change_in_elo = "+%d" % (elo_stop-elo_start)
            self.changed_elo_label_color = [0, 1, 0, 1]
        else:
            # Lost elo, make it red
            self.change_in_elo = "%d" % (elo_stop-elo_start)
            self.changed_elo_label_color = [1, 0, 0, 1]


    def open(self):
        Window.add_widget(self)
        self.add_fab()

        # Slide the menu up
        fab_y = (.5 - self.size_hint_y / 2.0) * Window.height - self.fab.height * 1.25
        anim = Animation(pos_hint={"center_y": .5, "center_x": .5},
                         transition='in_out_back')
        anim2 = Animation(y=fab_y, angle=0, transition='in_out_back')
        anim.start(self)
        anim2.start(self.fab)

        # Bring up a little button that lets the user see the board
        #Clock.schedule_once(self.add_fab, 0)

        self.is_open = True


    def add_fab(self, *args):
        fab = GameOverFab(on_release=self.show_or_hide_screen)
        fab.center_x = self.center_x
        fab.y = self.y - fab.height*1.25
        self.fab = fab
        fab.size_hint = (None, None)
        Window.add_widget(fab)

    def show_or_hide_screen(self, *args):
        if self.is_open:
            # Slide the menu down
            anim = Animation(pos_hint={"center_y": -self.size_hint_y, "center_x": .5}, transition='in_out_back')
            anim2 = Animation(y=0.25*self.fab.height, angle=180, transition='in_out_back')
            anim.start(self)
            anim2.start(self.fab)
            self.is_open = False
        else:
            # Slide the menu up
            fab_y = (.5-self.size_hint_y/2.0)*Window.height - self.fab.height*1.25
            anim = Animation(pos_hint={"center_y": .5, "center_x": .5}, transition='in_out_back')
            anim2 = Animation(y=fab_y, angle=0, transition='in_out_back')
            anim.start(self)
            anim2.start(self.fab)
            self.is_open = True

    def dismiss(self, to_lobby_browser_screen=False):
        """

        :param to_lobby_screen: if True, takes the player back to the lobby
        browser screen. Otherwise, just let's them play a new game
        :return:
        """
        anim = Animation(
            pos_hint={"center_y": -self.size_hint_y, "center_x": .5}, transition='in_out_back')
        anim2 = Animation(y=-self.fab.height, transition='in_out_back')
        if to_lobby_browser_screen:
            anim.bind(on_complete=self.back_to_lobby_browser)
        anim2.bind(on_complete=self.remove_self_and_fab)
        anim.start(self)
        anim2.start(self.fab)
        self.is_open = False

    def remove_self_and_fab(self, *args):
        Window.remove_widget(self.fab)
        Window.remove_widget(self)

    def back_to_lobby_browser(self, *args):
        app = App.get_running_app()
        app.change_screen("lobby_browser_screen")
        Window.remove_widget(self.fab)
        Window.remove_widget(self)

    def animate_elos(self, elo1_start, elo1_stop):
        self.player_elo = elo1_start
        anim = Animation(player_elo=elo1_stop, duration=3)
        anim.start(self)

    def revoke_or_request_rematch(self):
        app = App.get_running_app()

        if self.ids.player_is_ready_checkbox.active:
            # Ask the opponent to rematch
            message = {"command": "rematch_requested"}
            app.client.send_message(message)
            # If the enemy was already readied up, start the game
            if self.ids.opponent_is_ready_checkbox.active:
                app.root.ids.game_screen.accept_rematch()
        else:
            message = {"command": "revoke_rematch_request"}
            app.client.send_message(message)


    def leave_match(self):
        # Need to inform other player that this user left!
        app = App.get_running_app()
        message = {"command": "leave_match"}
        app.client.send_message(message)
        app.change_screen('lobby_browser_screen')
        self.dismiss()
        app.client.is_host = False



