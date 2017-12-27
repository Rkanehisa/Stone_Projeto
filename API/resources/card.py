from flask_restful import Resource, reqparse
from API.models.models import Card, User


class CardResource(Resource):
    @staticmethod
    def get(number):
        card = Card.get_by_number(number)
        if card:
            return card.json(), 200
        else:
            return {"Message": "Card not found"}, 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username", type=str, required=True)
        parser.add_argument("name", type=str, required=True)
        parser.add_argument("number", type=str, required=True)
        parser.add_argument("ccv", type=str, required=True)
        parser.add_argument("due_date", type=str, required=True)
        parser.add_argument("expiration_date", type=str, required=True)
        parser.add_argument("limit", type=str, required=True)

        args = parser.parse_args()

        if User.get_by_username(args["username"]):
            if Card.get_by_number(number=args["number"]):
                return {"Message": "Card already exists"}, 400
            else:
                card = Card(**args)
                card.save_in_db()
                user = User.get_by_username(args["username"])
                user.set_limit(float(args["limit"]) + user.get_limit())
                user.save_in_db()
                return card.json(), 201
        else:
            return {"Message": "User does not exists"}
