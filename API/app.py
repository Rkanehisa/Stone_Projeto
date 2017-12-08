from flask import Flask
from flask_restful import Api
from API.resources.user import UserResouce


app = Flask(__name__)
app.config.from_object("config.TestingConfig")

api = Api(app)

api.add_resource(UserResouce, "/user/register")
api.add_resource(UserResouce, "/user/<string:username>", endpoint='user')

