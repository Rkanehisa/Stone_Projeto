from API.models.models import User


def verify(username, password):
    if not (username and password):
        return False
    user = User.get_by_username(username)
    if user is not None:
        user.verify_password(password)
        return user.json()


def identity(payload):
    user_id = payload['identity']
    return {"user_id": user_id}