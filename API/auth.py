from API.models.models import User


def authenticate(username, password):
    # if not (username and password):
    #    return False
    user = User.get_by_username(username)
    if user is not None:
        if user.verify_password(password):
            return user
        else:
            return {"message": "username or password if incorrect", "id": -1}


def identity(payload):
    user_id = payload['identity']
    return User.get_by_id(user_id)
