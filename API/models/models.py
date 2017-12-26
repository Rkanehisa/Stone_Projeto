from API.db import db
from datetime import datetime


class Card(db.Model):
    __tablename__ = "card"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    number = db.Column(db.String(16), nullable=False)
    ccv = db.Column(db.String(3), nullable=False)
    due_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    expiration_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    limit = db.Column(db.Float, nullable=False)

    wallet_id = db.Column(db.Integer, db.ForeignKey("wallet.id"), nullable=False)
    wallet = db.relationship("Wallet", back_populates="card")

    def __init__(self, username, name, number, ccv, due_date, expiration_date, limit):
        user = User.query.filter_by(username=username).first()
        self.wallet = Wallet.query.filter_by(user_id=user.id).first()
        self.name = name
        self. number = number
        self.ccv = ccv
        self.due_date = due_date
        self.expiration_date = expiration_date
        self.limit = limit


class Wallet(db.Model):
    __tablename__ = "wallet"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    limit = db.Column(db.Float, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", back_populates="wallet")

    card = db.relationship("Card", uselist=False, back_populates="wallet", cascade='all, delete')

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

    def set_limit(self, limit):
        self.limit = limit


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)

    wallet = db.relationship("Wallet", uselist=False, back_populates="user", cascade='all, delete')

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
