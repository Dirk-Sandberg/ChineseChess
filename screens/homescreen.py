from kivy.uix.screenmanager import Screen
from kivy.app import App


class HomeScreen(Screen):
    def start_local_game(self):
        app = App.get_running_app()
        app.root.ids.game_screen.online_mode_enabled = False
        app.root.current = 'game_screen'



