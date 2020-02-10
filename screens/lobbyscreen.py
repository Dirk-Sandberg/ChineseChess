from kivy.uix.screenmanager import Screen
from kivy.app import App


class LobbyScreen(Screen):
    def back_to_lobby_browser(self):
        self.ids.player_two.text = "Waiting for an opponent..."

        app = App.get_running_app()
        app.change_screen('lobby_browser_screen')
        message = {"command": "leave_match", 'is_host': app.client.is_host}
        app.client.send_message(message)

    def player_two_left(self):
        print("AAAAY player two left")
        self.ids.player_two.text = "Waiting for an opponent..."

    def start_match(self):
        # Send a message to the server that the game is started
        app = App.get_running_app()
        message = {"command": "start_match"}
        app.client.send_message(message)
        # When the game starts, it will send a message back to both players
        # which will change the screen to the game screen