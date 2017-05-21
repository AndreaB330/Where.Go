from app import *
from model import *
from flask import render_template, jsonify
import json

@app.route('/category/<cid>')
def category(cid):
    c = Category.query.filter_by(id=cid).first_or_404()
    return jsonify(name=c.name)

@app.route('/events/<cid>')
def events(cid):
    c = Category.query.filter_by(id=cid).first_or_404()
    ls = c.locations.all()
    l = [{'name':x.name, 'lat':x.lat,'lon':x.lon} for l in ls]
    return json.dumps(l)

@app.route('/complete/<lid>')
def complete(lid):
    c = Completion(0, lid)
    db.session.add(c)
    db.session.commit()
