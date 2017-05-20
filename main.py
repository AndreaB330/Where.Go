from app import *
from flask import render_template

Kyiv = {'lat':50.45,'lng':30.52}

@app.route('/')
def homepage():
    return render_template('index.html', API_KEY = app.config['API_KEY'],  center=Kyiv)

