from kivy.uix.screenmanager import Screen
from kivy.app import App


class LobbyScreen(Screen):
    def start_match(self):
        # Send a message to the server that the game is started
        app = App.get_running_app()
        message = {"command": "start_match"}
        app.client.send_message(message)
        # When the game starts, it will send a message back to both players
        # which will change the screen to the game screen