from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivymd.uix.list import TwoLineListItem

class LobbyItem(TwoLineListItem):
    host_elo = ""
    def on_release(self):
        # Tell the server that we are joining the lobby
        app = App.get_running_app()
        app.player.game_id = self.game_id
        message = {"command": "join_game"}
        app.client.send_message(message)
        # Set the opponents host elo so we can change elo when game is over
        #TODO
        # Should this be done after receiving the message back from the server?
        app.player.opponent_elo = self.host_elo


class LobbyBrowserScreen(Screen):
    def get_lobbies_from_server(self):
        app = App.get_running_app()
        message = {"command": "get_lobbies"}
        app.client.send_message(message)

    def display_lobbies(self, lobbies_list):
        self.ids.list_layout.clear_widgets()
        for lobby in lobbies_list:
            game_id = lobby['game_id']
            name = lobby['host_name']
            host_elo = str(lobby['host_elo'])
            time_limit = str(lobby['time_limit'])
            lobby_item = LobbyItem(text=name + "'s Match, rating " + host_elo,
                                         secondary_text="Time Limit: " + time_limit + " minutes")
            lobby_item.game_id = game_id
            lobby_item.host_elo = host_elo
            self.ids.list_layout.add_widget(lobby_item)

