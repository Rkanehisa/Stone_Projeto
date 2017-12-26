from flask_restful import Resource,reqparse
from API.models.models import Wallet,User


class WalletResouce(Resource):
    def get(self, username):
        wallet = Wallet.get_by_username(username)
        if wallet:
            return wallet.json(), 200
        else:
            return {"Message": "Wallet not found"}, 404

    def post(self, username):
        parser = reqparse.RequestParser()
        parser.add_argument("username", type=str, required=True)
        args = parser.parse_args()

        print(User.get_by_username(args["username"]))
        if User.get_by_username(args["username"]) is not None:
            if Wallet.get_by_username(args["username"]):
                return {"Message": "Wallet already exists"}, 400
            else:
                wallet = Wallet(args["username"])
                wallet.save_in_db()
                return wallet.json(), 201
        else:
            return {"Message": "User does not exists"}, 404
