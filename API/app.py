from flask import Flask
from flask_restful import Api
from API.resources.user import UserResouce
from API.resources.wallet import WalletResouce


app = Flask(__name__)
app.config.from_object("config.TestingConfig")

api = Api(app)


# User URLs
api.add_resource(UserResouce, "/user/register")
api.add_resource(UserResouce, "/user/<string:username>", endpoint='user')

# Wallet URLs
api.add_resource(WalletResouce,"/wallet/create<string:username>")
api.add_resource(WalletResouce,"/wallet/<string:username>", endpoint='wallet')
