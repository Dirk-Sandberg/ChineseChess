from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivymd.toast import toast


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
        app.root.ids.firebase_login_screen.display_loading_screen()

    def nickname_was_valid(self):
        app = App.get_running_app()
        app.player.set_nickname(self.nickname)
        app.root.ids.firebase_login_screen.hide_loading_screen()

    def nickname_was_invalid(self):
        app = App.get_running_app()
        toast('That name is already taken')
        app.root.ids.firebase_login_screen.hide_loading_screen()

