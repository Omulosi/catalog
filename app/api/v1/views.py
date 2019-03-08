"""
app.api.v1.views
~~~~~~~~~~~~~~~~~
RESTFul API for Item model

"""

from flask_restful import Resource
from . import api

class ItemAPI(Resource):
    
    def get(self, id=None):
        # Return item data
        pass

    def post(self):
        # create new item
        pass

    def put(self, id):
        # update item with given ID
        pass

    def delete(self, id):
        # Delete item with given ID
        pass


api.add_resource(
    ItemAPI,
    '/items',
    '/items/<int: id>'
    )
