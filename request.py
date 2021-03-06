from app import *
from model import *
from flask import render_template, jsonify
import json

@app.route('/category/<cid>')
def category(cid):
    c = Category.query.filter_by(id=cid).first_or_404()
    return jsonify(name=c.name, short_name=c.short_name)

@app.route('/events/<cid>')
def events(cid):
    c = Category.query.filter_by(id=cid).first_or_404()
    ls = c.locations
    co = Completion.query.filter_by(uid=1).all()
    cs = [l.lid for l in co]
    l = [{'id': x.id, 'name':x.name, 'lat':x.lat,'lon':x.lon, 'rating': x.rating, 'complete': x.id in cs} for x in ls]
    return json.dumps(sorted(l, key=lambda x:x['rating']*-1))

@app.route('/complete/<lid>')
def complete(lid):
    c = Completion(1, lid)
    db.session.add(c)
    db.session.commit()
    return json.dumps({'success': 1})
    
@app.route('/clear')
def clear():
    Completion.query.delete()
    db.session.commit()
    return json.dumps({'success': 1})
