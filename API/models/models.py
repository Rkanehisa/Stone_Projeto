from API.db import db
from datetime import datetime
from passlib.apps import custom_app_context as pwd_context


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)

    limit = db.Column(db.Float, nullable=False)  # Sum of limits from all cards
    user_limit = db.Column(db.Float, nullable=False)  # Limit defined by user
    cards = db.relationship("Card", cascade='all, delete', lazy='dynamic')

    def __init__(self, username, password):
        self.username = username
        self.password = pwd_context.encrypt(password)
        self.limit = 0
        self.user_limit = 0

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)

    def json(self):
        return {"id": self.id, "username": self.username, "password": str(self.password), "limit": self.limit,
                "user limit": self.user_limit, "spent_limit": self.get_spent()}

    def save_in_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, user_id):
        return cls.query.filter_by(id=user_id).first()

    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    def get_limit(self):
        return self.limit

    def get_user_limit(self):
        return self.user_limit

    def set_limit(self, limit):
        self.limit = limit

    def set_user_limit(self, limit):
        self.user_limit = limit

    def get_cards(self):
        return self.cards

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def get_cards(self):
        return self.cards.order_by(Card.spent_limit).all()

    def get_spent(self):
        return sum(x.spent_limit for x in self.cards.all())




class Card(db.Model):
    __tablename__ = "card"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    number = db.Column(db.String(16), nullable=False)
    ccv = db.Column(db.String(3), nullable=False)
    due_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    expiration_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    limit = db.Column(db.Float, nullable=False)
    spent_limit = db.Column(db.Float, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", back_populates="cards")

    def __init__(self, username, name, number, ccv, due_date, expiration_date, limit):
        # Parse strings to convert to to datetime
        datetime_due_date = datetime.strptime(due_date, "%Y/%m/%d")
        datetime_expiration_date = datetime.strptime(expiration_date, "%Y/%m/%d")

        self.user_id = User.query.filter_by(username=username).first().id
        self.name = name
        self. number = number
        self.ccv = ccv
        self.due_date = datetime_due_date
        self.expiration_date = datetime_expiration_date
        self.limit = limit
        self.spent_limit = 0

    def json(self):
        return {"id": self.id, "name": self.name, "number": self.number, "ccv": self.ccv,
                "due_date": str(self.due_date), "expiration_date": str(self.expiration_date), "limit": self.limit,
                "spent limit": self.spent_limit, "user_id": self.user_id}

    def save_in_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_number(cls, number):
        return cls.query.filter_by(number=number).first()

    def get_limit(self):
        return self.limit

    def get_spent_limit(self):
        return self.spent_limit

    def set_spent_limit(self, spent_limit):
        self.spent_limit = spent_limit

    def delete(self):
        user = User.query.filter_by(id=self.user_id).first()
        user.set_limit(user.limit-self.limit)
        db.session.delete(self)
        db.session.commit()
