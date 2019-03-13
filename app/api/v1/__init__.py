
from flask import Blueprint
from flask_restful import Api

bp = Blueprint('catalog', __name__)
api = Api(bp)

from .items import ItemAPI
from .auth import SignUP, SignIn, RefreshToken
from .tokens import Tokens

# routes for item resource
api.add_resource(
    ItemAPI,
    '/items',
    '/items/<id>',
    '/items/<id>/<field>',
    endpoint='item'
    )
# Authenticaion routes
api.add_resource(
        SignUP,
        '/auth/signup',
        )

api.add_resource(
        SignIn,
        '/auth/signin',
        )

api.add_resource(
        RefreshToken,
        '/auth/refresh',
        )

api.add_resource(
        Tokens,
        '/auth/tokens',
        '/auth/tokens/<token_id>'
        )
