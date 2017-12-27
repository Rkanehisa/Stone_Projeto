from flask_restful import Resource, reqparse
from API.models.models import User


class UserResouce(Resource):
    @staticmethod
    def get(username):
        user = User.get_by_username(username)
        if user:
            return user.json(), 302
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

    @staticmethod
    def patch(username):
        parser = reqparse.RequestParser()
        parser.add_argument("user_limit", type=float, required=False)
        args = parser.parse_args()

        user = User.get_by_username(username)
        if user is not None:
            if "user_limit" in args:
                if user.get_limit() < float(args["user_limit"]):
                    user.set_user_limit(float(args["user_limit"]))
                else:
                    return {""}
            user.save_in_db()
            return user.json(), 200

        else:
            return {"message": "User not found"}, 404
