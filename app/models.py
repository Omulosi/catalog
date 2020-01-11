from datetime import datetime
from . import db, bcrypt


class User(db.Model):
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(140))
    firstname = db.Column(db.String(64), default='')
    lastname = db.Column(db.String(64), default='')
    bank_name = db.Column(db.String(64), default='')
    role = db.Column(db.String(64), default='')
    admin = db.Column(db.Boolean, default=False)
    createdon = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    farm = db.relationship('Farm', backref='farms', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    @property
    def serialize(self):
        return {'id': self.id,
                'email': self.email,
                'firstname': self.firstname,
                'lastname': self.lastname,
                'role': self.role,
                'createdon': self.createdon.strftime('%a, %d %b %Y %H:%M %p'),
                'bank_name': self.bank_name
                }


    def __repr__(self):
        return '<User {}>'.format(self.email)


class Farm(db.Model):

    __tablename__ = 'farms'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(300))
    stage = db.Column(db.String(64), default="closed") # open/closed
    harvest_time = db.Column(db.DateTime) # year, month, day
    location = db.Column(db.String(64))
    units = db.Column(db.Integer) # No of units in the farm
    margin = db.Column(db.Float) # Expected profit margin
    active = db.Column(db.Boolean, default=False) # operates when active only
    createdon = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    @property
    def serialize(self):

        return {'id': self.id,
                'name': self.name,
                'location': self.location,
                'units': self.units,
                'active': self.active,
                'harvest_time': self.harvest_time and self.harvest_time.strftime('%a, %d %b %Y'),
                'margin': self.margin,
                'stage': self.stage,
                'description': self.description,
                'createdon': self.createdon.strftime('%a, %d %b %Y %H:%M %p'),
                'createdby': self.user_id
                }

    def __repr__(self):
        return '<Farm {}>'.format(self.farm_name)


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
