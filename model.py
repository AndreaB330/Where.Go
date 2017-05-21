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

def sqlpls(src, stmt, **params):
        return db.session.query(src).from_statement(text(stmt)).params(**params).all()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(128), unique=True)
    salt = db.Column(db.String(16), nullable=False)
    hash = db.Column(db.String(64), nullable=False)
    completions = db.relationship('Completion', backref='user', lazy='dynamic')

    def try_complete(self, quest, lat, lon):
        if quest.location.check_inside(lat, lon):
            c = Completion(self.id, quest.id)
            db.session.add(c)
            db.session.commit()
            return True
        return False

    def incomplete_in_cat(self, category):
        return sqlpls(Location, "SELECT * FROM quest WHERE quest.cat_id = :cid AND quest.id NOT IN (SELECT qid FROM completion WHERE quest.uid = :uid)", cid=category.id, uid=self.id)

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

quest=db.Table('quest',
        db.Column('loc_id', db.Integer, db.ForeignKey('location.id')),
        db.Column('cat_id', db.Integer, db.ForeignKey('category.id')),
        )

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128))
    rating = db.Column(db.Float)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)

    def check_inside(self, lat, lon):
        return math.sqrt((self.lat - lat) ** 2 + (self.lon - lon) ** 2) <= EPS

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128))
    locations = db.relationship('Location', secondary=quest,
            backref=db.backref('categories', lazy='dynamic'))

class Completion(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.Integer, db.ForeignKey('user.id'))
    lid = db.Column(db.Integer, db.ForeignKey('location.id'))

    def __init__(self, uid ,lid):
        self.uid = uid
        self.lid = lid
