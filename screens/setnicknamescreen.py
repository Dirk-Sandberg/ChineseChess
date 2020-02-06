from kivy.uix.screenmanager import Screen
from kivy.app import App


class SetNicknameScreen(Screen):
    def set_nickname(self, nickname):
        print("Setting the player's nickname in firebase to: ", nickname)
        app = App.get_running_app()
        app.player.set_nickname(nickname)

