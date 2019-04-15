from datetime import datetime
from . import db, bcrypt

class User(db.Model):
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, default='')
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(140))
    firstname = db.Column(db.String(64), default='')
    lastname = db.Column(db.String(64), default='')
    admin = db.Column(db.Boolean, default=False)
    createdon = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    items = db.relationship('Item', backref='createdby', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    @property
    def serialize(self):
        return {'id': self.id,
                'username': self.username,
                'email': self.email,
                'firstname': self.firstname,
                'lastname': self.lastname,
                'admin': self.admin,
                'createdon': self.createdon.strftime('%a, %d %b %Y %H:%M %p')
                }


    def __repr__(self):
        return '<User {}>'.format(self.username)

class Item(db.Model):

    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    itemname = db.Column(db.String(64))
    description = db.Column(db.String(300))
    category = db.Column(db.String(64), index=True)
    createdon = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    @property
    def serialize(self):
        return {'id': self.id,
                'itemname': self.itemname,
                'category': self.category,
                'description': self.description,
                'createdon': self.createdon.strftime('%a, %d %b %Y %H:%M %p'),
                'createdby': self.user_id
                }

    def __repr__(self):
        return '<Item {}>'.format(self.itemname)


class TokenBlacklist(db.Model):

    __tablename__ = 'token_blacklist'

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(50), nullable=False)
    token_type = db.Column(db.String(10), nullable=False)
    user_identity = db.Column(db.String(50), nullable=False)
    revoked = db.Column(db.Boolean, nullable=False)
    expires = db.Column(db.DateTime, nullable=False)

    @property
    def serialize(self):
        return {
            'token_id': self.id,
            'jti': self.jti,
            'token_type': self.token_type,
            'user_identity': self.user_identity,
            'revoked': self.revoked,
            'expires': self.expires.strftime('%a, %d %b %Y %H:%M %p')
        }
