#import certifi
from requests import patch, get
FIREBASE_URL = "https://chinese-chess-6543e.firebaseio.com/"


def check_if_new_player(firebase_id, idToken):
    # Check if this player has an `elo` attribute before setting it to the
    # new player elo of 1200. This makes sure people can't call this function
    # to update their elo to 1200 at any time.
    req = get(FIREBASE_URL+firebase_id+"/elo.json?auth=%s"%idToken)
    # req.json() will be None if they are new
    return not req.json()



def set_elo(firebase_id, new_elo, idToken):
    """Set elo for both players of a game

    :param elo:
    :param idToken: auth token of admin firebase account
    :return:
    """
    new_elo = '{"elo": %s}' %new_elo
    # Firebase rules allow the server's auth token to update all players' elos

    req = patch(FIREBASE_URL+firebase_id+".json?auth=%s"%idToken, new_elo)
    print(req.content)


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
