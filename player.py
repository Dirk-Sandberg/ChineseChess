from kivy.utils import platform
from kivy.event import EventDispatcher
from kivy.properties import BooleanProperty, NumericProperty
from kivy.network.urlrequest import UrlRequest
from kivy.app import App
import certifi
from json import dumps
from kivy.clock import mainthread
from elo import rate_1vs1

class Player(EventDispatcher):
    nickname = ""
    opponent_nickname = ""
    is_red = BooleanProperty(False)  # Player is either red or black
    game_id = ""  # Could replace the game id in the client code
    elo = 0
    opponent_elo = 0
    time_limit = NumericProperty(0)

    @mainthread
    def update_elo_after_match_ends(self, checkmated_player_color):
        print(checkmated_player_color, 'LOST')
        if checkmated_player_color == 'red' and self.is_red or checkmated_player_color == 'black' and not self.is_red:
            loser_elo = self.elo
            winner_elo = self.opponent_elo
        else:
            loser_elo = self.opponent_elo
            winner_elo = self.elo
        #host doesn't set opponents elo
        new_winner_elo, new_loser_elo = rate_1vs1(winner_elo, loser_elo)

        # Update the player's elo in firebase.
        if checkmated_player_color == 'red' and self.is_red or checkmated_player_color == 'black' and not self.is_red:
            new_elo = int(new_loser_elo)
        else:
            new_elo = int(new_winner_elo)
        loser_elo, new_loser_elo = int(loser_elo), int(new_loser_elo)
        winner_elo, new_winner_elo = int(winner_elo), int(new_winner_elo)
        self.set_elo(new_elo)
        print("My new elo is", new_elo)

        # Tell the game screen to open the game over dialog popup
        app = App.get_running_app()
        winner_color = 'red' if checkmated_player_color == 'black' else 'black'
        app.root.ids.game_screen.display_game_over_dialog(winner_color, loser_elo, new_loser_elo, winner_elo, new_winner_elo,
                           self.nickname, self.opponent_nickname)
        app.root.ids.game_screen.game_is_playing = False

    def retrieve_elo_from_firebase(self):
        app = App.get_running_app()
        local_id = app.root.ids.firebase_login_screen.localId
        UrlRequest(app.firebase_url + local_id + "/elo.json",
                   ca_file=certifi.where(),
                   on_success=self.got_elo_from_firebase,
                   on_failure=self.failed_to_get_elo_from_firebase,
                   on_error=self.failed_to_get_elo_from_firebase)

    def got_elo_from_firebase(self, thread, elo):
        self.elo = int(elo)

    def failed_to_get_elo_from_firebase(self, *args):
        print("failed_to_get_elo_from_firebase", args)
        pass

    def set_elo(self, elo):
        new_elo = '{"elo": %s}' %elo
        app = App.get_running_app()
        local_id = app.root.ids.firebase_login_screen.localId
        UrlRequest(App.get_running_app().firebase_url + local_id + ".json",
                   req_body=new_elo, method='PATCH', ca_file=certifi.where(),
                    on_success=self.updated_elo,
                    on_failure=self.failed_to_update_elo,
                    on_error=self.failed_to_update_elo)

    def updated_elo(self, thread, elo_data):
        self.elo = elo_data['elo']

    def failed_to_update_elo(self, *args):
        print("failed_to_update_elo", *args)

    def set_nickname(self, nickname):
        """Overwrites the nickname saved firebase for this player

        :param nickname: The new nickname to save
        """
        print("Trying to update the nickname in firebase to", nickname)
        nickname_data = {"nickname": nickname}
        nickname_data = dumps(nickname_data)
        app = App.get_running_app()
        local_id = app.root.ids.firebase_login_screen.localId
        UrlRequest(app.firebase_url + local_id + ".json",
                   req_body=nickname_data, method='PATCH', ca_file=certifi.where(),
                   on_success=self.updated_nickname,
                   on_failure=self.failed_to_update_nickname,
                   on_error=self.failed_to_update_nickname)

    def updated_nickname(self, thread, nickname_data):
        app = App.get_running_app()
        app.root.current = 'home_screen'
        self.nickname = nickname_data['nickname']


    def failed_to_update_nickname(self, *args):
        print("failed_to_update_nickname", args)

    def get_saved_nickname(self):
        """Gets the saved nickname from firebase

        """
        app = App.get_running_app()
        local_id = app.root.ids.firebase_login_screen.localId
        UrlRequest(app.firebase_url + local_id + "/nickname.json",
                   ca_file=certifi.where(),
                   on_success=self.got_saved_nickname,
                   on_failure=self.failed_to_get_saved_nickname,
                   on_error=self.failed_to_get_saved_nickname)

    def got_saved_nickname(self, thread, nickname):
        self.nickname = nickname

    def failed_to_get_saved_nickname(self, *args):
        print("failed_to_get_saved_nickname", args)

