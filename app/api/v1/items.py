"""
app.api.v1.views
~~~~~~~~~~~~~~~~~
RESTFul API for Item model

"""

from flask_restful import Resource, reqparse, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Item
from app import db
from .common.errors import raise_error
from .common.utils import valid_item_name, valid_category, valid_description

parser = reqparse.RequestParser()
parser.add_argument('itemname', type=str)
parser.add_argument('category', type=str)
parser.add_argument('description', type=str)

class ItemAPI(Resource):
    
    @jwt_required
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
        if not valid_description(description):
            return raise_error(400, "Invalid description")

        item = Item(itemname=item_name, category=category, description=description)
        db.session.add(item)
        db.session.commit()
        uri = url_for('catalog.item', id=item.id, _external=True)

        output = {}
        output['status'] = 201
        output['message'] = 'Created a new item'
        data = item.serialize
        data['uri'] = uri
        output['data'] = [data]

        return output, 201, {'Location': uri}

    @jwt_required
    def get(self, id=None):
        # Return item data
        if id is None:
            # Return a collection of all items
            all_items = Item.query.all()
            output = {}
            output['status'] = 200
            data = all_items
            if all_items:
                data = [item.serialize for item in all_items]
            output['data'] = data

            return output

        if not id.isnumeric():
            return raise_error(400, "Item ID should be an integer")
        item_id = int(id)
        item = Item.query.get(item_id)
        if not item:
            return raise_error(404, "Requested item does not exist")

        output = {}
        output['status'] = 200
        output['data'] = [item.serialize]

        return output

    @jwt_required
    def patch(self, id, field):
        # update item with given ID
        if not id.isnumeric():
            return raise_error(400, "Item ID should be an integer")
        if field not in ('itemname', 'category', 'description'):
            return raise_error(400, "Invalid field name")

        parser = reqparse.RequestParser()
        parser.add_argument(field, type=str, required=True)

        try:
            args = parser.parse_args(strict=True)
        except:
            error_msg = "Invalid input data. Only {} field should be provided".format(field)
            return raise_error(400, error_msg)

        new_field_value = args.get(field)
        if field == 'itemname':
            new_field_value = valid_item_name(new_field_value)
        elif field == 'category':
            new_field_value = valid_category(new_field_value)
        elif field == 'description':
            new_field_value = valid_description(new_field_value)
        if not new_field_value:
            return raise_error(400, "{} field is invalid".format(field))

        item_id = int(id)
        item = Item.query.get(item_id)

        if not item:
            return raise_error(404, "Item does not exist")
        if field == 'itemname':
            item.itemname = new_field_value
        if field == 'description':
            item.description = new_field_value
        if field == "category":
            item.category = new_field_value

        db.session.commit()

        output = {}
        data = item.serialize
        output['status'] = 200
        data['message'] = 'successfully updated item {}'.format(field)
        output['data'] = [data]

        return output

    @jwt_required
    def delete(self, id):
        # Delete item with given ID
        if not id.isnumeric():
            return raise_error(400, "Item ID should be an integer")
        item_id = int(id)
        item = Item.query.get(item_id)
        if not item:
            return raise_error(404, "Item does not exist")
        db.session.delete(item)
        db.session.commit()

        output = {}
        message = 'Item has been deleted'
        output['status'] = 200
        output['data'] = [{'id': item_id, 'message': message}]
        return output
