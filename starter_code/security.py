from werkzeug.security import safe_str_cmp #to compar strings safely between Python 2 and 3
from models.user import UserModel


def authenticate(username, password):
    """
    This function gets called when a user calls the /auth endpoint with username and password.
    :param username:
    :param password: (Un encrypted)
    :return: A user model object if authentification was unsuccesful. None otherwise.
    """

    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    """
    this function gets called when user has already authentificated, and Flask-JWT verified the
    authentification header is correct. It provides the payload varaible
    :param payload: Dictionary with 'identity key", which is the user ID
    :return: A UserModel object
    """
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
