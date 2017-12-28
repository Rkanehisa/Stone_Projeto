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
                if user.user_limit == 0:
                    user.set_user_limit(float(args["limit"]))

                user.save_in_db()
                return card.json(), 201
        else:
            return {"Message": "User does not exists"}

    @staticmethod
    def patch(number):
        parser = reqparse.RequestParser()
        parser.add_argument("value", type=float, required=False)
        args = parser.parse_args()

        card = Card.get_by_number(number)
        if card is not None:
            if "value" in args:
                if card.get_spent_limit()+float(args["value"]) <= card.get_limit():
                    card.set_spent_limit(card.get_spent_limit()+float(args["value"]))
                else:
                    return {"message": "transaction not authorized"}, 304
            card.save_in_db()
            return card.json()

        else:
            return {"message": "Card not found"}, 404

    def delete(self, number):
        card = Card.get_by_number(number)
        if card is not None:
            card.delete()
            return {"message": "Card deleted"}, 200
        else:
            return {"message": "Card not found"}, 404
