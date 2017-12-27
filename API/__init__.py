from flask import  Flask
from flask_restful import Api
from API.resources.user import UserResouce
from API.resources.card import CardResource

app = Flask(__name__)
app.config.from_object("config.DevelopmentConfig")

api = Api(app)

# User URLs
api.add_resource(UserResouce, "/user/register",
                 "/user/<string:username>",
                 "/user/<string:username>/edit",
                 endpoint='user')

# Card URLs
api.add_resource(CardResource, "/card/create",
                 "/card/<string:number>",
                 "/card/<string:number>/edit",
                 endpoint='card')