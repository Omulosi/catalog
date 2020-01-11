from flask import Blueprint
from flask_restful import Api

bp = Blueprint('one-acre', __name__)
api = Api(bp)

from .farms import FarmAPI
from .auth import SignUP, SignIn, RefreshToken
from .tokens import Tokens

# routes for farm resource
api.add_resource(
    FarmAPI,
    '/farms',
    '/farms/<id>',
    '/farms/<id>/<field>',
    endpoint='farm'
    )
# Authenticaion routes
api.add_resource(
        SignUP,
        '/auth/register',
        )

api.add_resource(
        SignIn,
        '/auth/login',
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
