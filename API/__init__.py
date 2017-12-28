from flask import  Flask
from flask_restful import Api
from API.resources.user import UserResouce
from API.resources.card import CardResource
from flask_jwt import JWT
from API.auth import verify, identity


app = Flask(__name__)
app.config.from_object("config.DevelopmentConfig")

api = Api(app)
jwt = JWT(app, verify, identity)


# User URLs
api.add_resource(UserResouce, "/user/register",
                 "/user/<string:username>",
                 "/user/<string:username>/edit",
                 "/user/<string:username>/delete",
                 endpoint='user')

# Card URLs
api.add_resource(CardResource, "/card/create",
                 "/card/<string:number>",
                 "/card/<string:number>/edit",
                 "/card/<string:number>/delete",
                 endpoint='card')