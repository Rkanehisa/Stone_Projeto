from flask import Flask
from flask_restful import Api
from API.resources.user import UserResouce
from API.resources.card import CardResource

app = Flask(__name__)
app.config.from_object("config.TestingConfig")

api = Api(app)


# User URLs
api.add_resource(UserResouce, "/user/register")
api.add_resource(UserResouce, "/user/<string:username>")
api.add_resource(UserResouce, "/user/<string:username>/edit")

# Card URLs
api.add_resource(CardResource, "/card/create")
api.add_resource(CardResource, "/card/<string:number>", endpoint='card')
