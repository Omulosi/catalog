"""
app.api.v1.views
~~~~~~~~~~~~~~~~~
RESTFul API for Item model

"""

from flask_restful import Resource, reqparse, url_for
from app.models import Item
from app import db
from .common.errors import raise_error
from .common.utils import valid_item_name, valid_category

parser = reqparse.RequestParser()
parser.add_argument('itemname', type=str, help='item name not provided')
parser.add_argument('category', type=str, help='category not provided')
parser.add_argument('description', type=str, help='description not provided')

class ItemAPI(Resource):
    
    def post(self):
        # create new item
        args = parser.parse_args()
        item_name = args['itemname']
        category = args['category']
        description = args['description']

        # Validate inout data
        if not valid_item_name(item_name):
            return raise_error(400, "Invalid item name")
        if not valid_category(category):
            return raise_error(400, "Invalid category name")
        if not description:
            return raise_error(400, "Invalid description")

        item = Item(itemname=item_name, category=category, description=description)
        db.session.add(item)
        db.session.commit()

        output = {}
        output['status'] = 201
        data = item.serialize
        data['message'] = 'Created a new item'
        output['data'] = [data]

        uri = url_for('catalog.item', id=item.id, _external=True)

        return output, 201, {'Location': uri}

    def get(self, id=None):
        # Return item data
        return {}

    def patch(self, id):
        # update item with given ID
        return {}

    def delete(self, id):
        # Delete item with given ID
        return {}
