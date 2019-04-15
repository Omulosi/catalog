
from app import db
from app.models import Item, TokenBlacklist
from app.helpers import add_token_to_database


def test_create_items(app):

    with app.app_context():
        item1 = Item(itemname='stick', description='hockey stick', 
                category='hockey')
        item2 = Item(itemname='jersey', description='play uniforms',
                category='soccer')

        db.session.add(item1)
        db.session.add(item2)
        db.session.commit()

        items = Item.query.all()
        assert len(items) == 2
        assert item1.category == 'hockey'
        assert item2.category == 'soccer'
        assert bool(item1.createdby) is False
        assert bool(item2.createdby) is False

