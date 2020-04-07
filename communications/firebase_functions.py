#import certifi
from requests import patch
FIREBASE_URL = "https://chinese-chess-6543e.firebaseio.com/"


def set_elo(firebase_id, new_elo):
    """Set elo for both players of a game

    :param elo:
    :return:
    """
    new_elo = '{"elo": %s}' %new_elo
    req = patch(FIREBASE_URL+firebase_id+".json", new_elo)


def updated_elo(self, thread, elo_data):
    """Successfully updated elo.

    :param thread:
    :param elo_data:
    """
    self.elo = elo_data['elo']


def failed_to_update_elo(self, *args):
    """Failed to update elo

    :param args:
    """
    print("failed_to_update_elo", *args)
