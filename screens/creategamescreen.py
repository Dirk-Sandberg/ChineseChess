from kivy.uix.screenmanager import Screen
from kivy.app import App


class CreateGameScreen(Screen):
    def host_match(self, time_limit):
        app = App.get_running_app()

        # Send command to server
        message = {"command": "host_match"}
        app.client.send_message(message)

        # When the server receives the host match command, it'll send a
        # "match_hosted" command back to this client. That's where the screen
        # will change to the lobby screen.
