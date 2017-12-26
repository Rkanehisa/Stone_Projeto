from API.db import db


class Wallet(db.Model):
    __tablename__ = "wallet"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    limit = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", back_populates="wallet")

    def __init__(self, username):
        self.user = User.query.filter_by(username=username).first()
        self.limit = 0

    def json(self):
        return {"id": self.id, "user": self.user_id, "limit": self.limit}

    def save_in_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_by_username(cls,username):
        user = User.get_by_username(username)
        return cls.query.filter_by(user_id=user.id).first()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128),nullable=False)
    wallet = db.relationship("Wallet", uselist=False, back_populates="user" , cascade='all, delete')

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
