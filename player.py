from kivy.utils import platform
from kivy.event import EventDispatcher
from kivy.properties import BooleanProperty


class Player(EventDispatcher):
    nickname = ""
    #ip_and_port = ""  # "192.168.1.2:12345
    is_red = BooleanProperty(False)  # Player is either red or black
    game_id = ""  # Could replace the game id in the client code
    saved_nickname_filename = "nickname.txt"
    elo = ""

    def __init__(self):
        # Directories on iOS can be screwed up
        if platform == 'ios':
            self.saved_nickname_filename = self.user_data_dir + "/" + self.saved_nickname_filename

        self.nickname = self.get_saved_nickname()

        self.elo = self.retrieve_elo_from_firebase()

    def retrieve_elo_from_firebase(self):
        print("Need to retrieve elo from firebase")
        return 1200


    def set_nickname(self, nickname):
        """Overwrites the nickname saved in the :self.saved_nickname_filename:
        file.

        :param nickname: The new nickname to save
        """
        try:
            with open(self.saved_nickname_filename, 'w') as f:
                f.write(nickname)
        except Exception as e:
            print("Couldn't save nickname", e)
        print("Just set nickname to ", nickname)

    def get_saved_nickname(self):
        """Gets the saved nickname from the :self.saved_nickname_filename: file.

        :return: The saved filename as a string
        """
        try:
            with open(self.saved_nickname_filename, 'r') as f:
                nickname = f.read()
        except:
            nickname = ""
        return nickname


