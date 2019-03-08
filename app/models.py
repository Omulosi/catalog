from datetime import datetime
from . import db, bcrypt

class User(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(140))
    firstname = db.Column(db.String(64))
    lastname = db.Column(db.String(64))
    createdon = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    items = db.relationship('Item', backref='createdby', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Item(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    itemname = db.Column(db.String(64))
    description = db.Column(db.String(300))
    category = db.Column(db.String(64), index=True)
    createdon = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Item {}>'.format(self.itemname)
