"""
app.api.v1.auth
~~~~~~~~~~~~~~

Authentication views

"""

from flask_jwt_extended import (
    create_access_token, get_raw_jwt, jwt_required, create_refresh_token,
    get_jwt_identity, jwt_refresh_token_required
)
from flask_restful import Resource, reqparse
from flask import current_app
from app.models import User
from app import db
from app.helpers import (
    is_token_revoked, add_token_to_database, get_user_tokens,
    revoke_token, unrevoke_token,
)
from .common.utils import (valid_email, valid_password)
from .common.errors import raise_error

parser = reqparse.RequestParser()
parser.add_argument('email', type=str) 
parser.add_argument('password', type=str)

class SignUP(Resource):

    def post(self):
        args = parser.parse_args()
        email = args.get('email') or ''
        password = args.get('password') or ''

        # validate input data
        if not valid_email(email):
            return raise_error(400, "Invalid email format")
        if not valid_password(password):
            return raise_error(400, "Invalid password. Should be at least 5 "
                    "characters long and include a number and a special "
                    "character")

        user = User.query.filter_by(email=email).first()
        if user is not None:
            return raise_error(400, "User already exists")
        #: set username to be same as email if it's not provided
        user = User(email=email, username=email)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        # Create our JWTs
        access_token = create_access_token(identity=email)
        refresh_token = create_refresh_token(identity=email)

        # Store the tokens in our store with a status of not currently revoked.
        add_token_to_database(access_token, current_app.config['JWT_IDENTITY_CLAIM'])
        add_token_to_database(refresh_token, current_app.config['JWT_IDENTITY_CLAIM'])

        data = {}
        data['access_token'] = access_token
        data['refresh_token'] = refresh_token
        data['user'] = user.serialize

        response = {
                "status": 201,
                "data": [data]
                }

        return response, 201

class SignIn(Resource):

    def post(self):
        args = parser.parse_args()
        email = args.get('email', None)
        password = args.get('password', None)

        if email is None:
            return raise_error(400, "Missing 'email' in body")
        if password is None:
            return raise_error(400, "Missing 'password' in body")

        user = User.query.filter_by(email=email).first()
        if user is None or not user.check_password(password):
            return raise_error(401, "Bad email or password")
        
        # Create our JWTs
        access_token = create_access_token(identity=email)
        refresh_token = create_refresh_token(identity=email)

        # Store the tokens in our store with a status of not currently revoked.
        add_token_to_database(access_token,current_app.config['JWT_IDENTITY_CLAIM'])
        add_token_to_database(refresh_token,current_app.config['JWT_IDENTITY_CLAIM'])

        data = {}
        data['access_token'] = access_token
        data['refresh_token'] = refresh_token
        data['user'] = user.serialize

        response = {
                "status": 200,
                "data": [data]
                }

        return response

class RefreshToken(Resource):
    """
    Creates a refresh token and returns it as response to a
    post request from a client.
    """

    @jwt_refresh_token_required
    def post(self):
        """
        Returns a new access token
        """
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user)
        add_token_to_database(new_token, current_app.config['JWT_IDENTITY_CLAIM'])

        return {
            'status': 200,
            'data': [{'access_token': new_token
                     }]
            }
