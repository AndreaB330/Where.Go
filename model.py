from app import db
import hashlib
import random
import enum
import math

def hash(salt, password):
    data = salt.encode() + password.encode()
    for i in range(100):
        h = hashlib.sha256()
        h.update(data)
        data = h.digest()
    return h.hexdigest()

gen_salt = lambda: ''.join(chr(random.randint(32,126)) for i in range(16))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(128), unique=True)
    salt = db.Column(db.String(16), nullable=False)
    hash = db.Column(db.String(64), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.salt = gen_salt()
        self.hash = hash(self.salt, password)

    def __repr__(self):
        return '<User %r>' % self.username

    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.id)

# TODO: check
# maximal distance between two points to consider them to be in same place
EPS = 1e-6

class Quest(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    loc_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    cat_id = db.Column(db.Integer, db.ForeignKey('category.id'))

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128))
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    quests = db.relationship('Quest', backref=db.backref('location', lazy='joined'), lazy='dynamic')

    def check_inside(self, lat, lon):
        return math.sqrt((self.lat - lat) ** 2 + (self.lon - lon) ** 2) <= EPS

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128))
    locations = db.relationship('Location', secondary=Quest,
            backref=db.backref('categories', lazy='dynamic'))

class Completion(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.Integer, db.ForeignKey('user.id'), db.backref('completions', lazy='dynamic'))
    qid = db.Column(db.Integer, db.ForeignKey('quest.id'))
