
from flask import Blueprint
from flask_restful import Api

bp = Blueprint('catalog', __name__)
api = Api(bp)

from .views import ItemAPI

# routes for item resource
api.add_resource(
    ItemAPI,
    '/items',
    '/items/<id>',
    '/items/<id>/<field>',
    endpoint='item'
    )
