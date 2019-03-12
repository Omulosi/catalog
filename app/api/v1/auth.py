"""
app.api.v1.auth
~~~~~~~~~~~~~~

Authentication views

"""

from flask_jwt_extended import create_access_token
from flask_restful import Resource, reqparse
from .common.utils import (valid_email, valid_password)
from .common.errors import raise_error
from app.models import User
from app import db

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
        user = User(email=email)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        data = {}
        data['access_token'] = create_access_token(identity=email)
        data['user'] = user.serialize

        response = {
                "status": 201,
                "data": [data]
                }

        return response, 201

class SignIn(Resource):

    def post(self):
        args = parser.parse_args()
        email = args.get('email') or ''
        password = args.get('password') or ''

        if not valid_email(email):
            return raise_error(400, "Invalid email format")
        if not valid_password(password):
            return raise_error(400, "Invalid password. Should be at least 5 "
                    "characters long and include a number and a special "
                    "character")

        user = User.query.filter_by(email=email).first()
        if user is None:
            return raise_error(401, "Invalid email. This user does not exist")
        if not user.check_password(password):
            return raise_error(401, "Wrong password")

        data = {}
        data['access_token'] = create_access_token(identity=email)
        data['user'] = user.serialize

        response = {
                "status": 200,
                "data": [data]
                }

        return response
