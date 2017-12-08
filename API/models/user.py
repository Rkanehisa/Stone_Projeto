from API.db import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128),nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def json(self):
        return {"id": self.id, "username": self.username, "password": self.password}

    def save_in_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()