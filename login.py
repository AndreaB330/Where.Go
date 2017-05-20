from app import *
import model
from model import hash
from flask import render_template
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user

Kyiv = {'lat':50.45,'lng':30.52}

@app.route('/login', methods=['POST'])
def homepage():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    if user is None:
        return
    h = hash(user.salt, request.form['password'])
    if h != user.hash:
        return
    login_user(user)
    flash('Logged in successfully')

@app.route('/register', method=['POST']):
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    user = User.query.filter_by(username=request.form['username']).first()
    if user:
        flash('Duplicate user!','warning')
        return
    u = User(username, email, password)
    db.session.add(u)
    db.session.commit()
    return
