
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

def test_add_token_to_blacklist(app, auth):

    auth.signup()
    access_token = auth.access_token
    refresh_token = auth.refresh_token

    with app.app_context():
        
        add_token_to_database(access_token, app.config['JWT_IDENTITY_CLAIM'])
        add_token_to_database(refresh_token, app.config['JWT_IDENTITY_CLAIM'])

        tokens = TokenBlacklist.query.all()
        for t in tokens:
            print(t.serialize)
        assert len(tokens) == 2


