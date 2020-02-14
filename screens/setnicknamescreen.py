from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivymd.toast import toast
from kivy.network.urlrequest import UrlRequest
import certifi

class SetNicknameScreen(Screen):
    nickname = ''

    def set_nickname(self, nickname):
        self.nickname = nickname
        if ',' in nickname:
            toast("Nicknames can't contain commas")
            return
        app = App.get_running_app()
        message = {'command': 'check_nickname_avail', 'nickname': nickname}
        app.client.send_message(message)
        print("firebase login screen loading circle here")

    def nickname_was_valid(self):
        app = App.get_running_app()
        app.player.set_nickname(self.nickname)

    def nickname_was_invalid(self):
        toast('That name is already taken')

