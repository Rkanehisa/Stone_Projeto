from flask import  Flask
from flask_restful import Api
from flask_jwt import JWT
from API.auth import authenticate, identity


app = Flask(__name__)
app.config.from_object("config.TestingConfig")

api = Api(app)
jwt = JWT(app, authenticate, identity)