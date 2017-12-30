from flask_restful import Resource, reqparse
from API.models.models import User
from flask_jwt import jwt_required


class PaymentResources(Resource):

    @staticmethod
    @jwt_required()
    def post():
        parser = reqparse.RequestParser()
        parser.add_argument("user_id", type=int, required=True)
        parser.add_argument("value", type=float, required=True)
        args = parser.parse_args()

        user = User.get_by_id(args["user_id"])

        if user is not None:
            cards = user.get_cards()
            if len(cards) != 0:
                if user.get_user_limit() >= user.get_spent() + float(args["value"]):
                    for card in cards:
                        print(card, card.limit, card.spent_limit)
                        if card.limit >= card.get_spent_limit()+float(args["value"]):
                            card.set_spent_limit(card.get_spent_limit() + float(args["value"]))
                            card.save_in_db()
                            return card.json(), 200
                    return {"message": "payment exceeds cards limits"}, 400
                else:
                    return {"message": "payment exceeds user limit"}, 400
            else:
                return {"message": "user has no cards"}, 400
        else:
            return {"message": "user not found"}, 404
