from flask_restful import Resource, reqparse
from API.models.models import User


class UserResouce(Resource):
    @staticmethod
    def get(username):
        user = User.get_by_username(username)
        if user:
            return user.json(), 200
        else:
            return {"Message": "User not found"}, 404

    @staticmethod
    def post():
        parser = reqparse.RequestParser()
        parser.add_argument("username", type=str, required=True)
        parser.add_argument("password", type=str, required=True)
        args = parser.parse_args()

        if User.get_by_username(args["username"]):
            return {"Message": "Username already exists"}, 400
        else:
            user = User(**args)
            user.save_in_db()
            return user.json(), 201

    def patch(self):
        parser = reqparse.RequestParser()
