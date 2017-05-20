from app import db
import hashlib
import random
import enum

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

    def __init__(self, username, name, email, password):
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
        return True
    
    def get_id(self):
        return str(self.id)

