from flask import  Flask, jsonify
from flask_restful import Api
from API.resources.user import UserResource
from API.resources.card import CardResource
from API.resources.payment import PaymentResources
from flask_jwt import JWT, JWTError
from API.auth import authenticate, identity


app = Flask(__name__)
app.config.from_object("config.DevelopmentConfig")

api = Api(app)
jwt = JWT(app, authenticate, identity)


# User URLs
api.add_resource(UserResource, "/user/register",
                 "/user/<string:username>",
                 "/user/<string:username>/edit",
                 "/user/<string:username>/delete",
                 endpoint='user')

# Card URLs
api.add_resource(CardResource, "/card/create",
                 "/card/<string:number>",
                 "/card/<string:number>/edit",
                 "/card/<string:number>/delete",
                 endpoint='card')

# Payment URLs
api.add_resource(PaymentResources, "/payment",
                 endpoint='payment')

@app.errorhandler(JWTError)
def authorization_error_handler(err):
    return jsonify(
        {
            "message": "Error while authorizing, you must include and Authorization Header."
        }
), 401
