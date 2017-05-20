from flask import Flask,render_template
app = Flask(__name__)

Kyiv = {'lat':50.45,'lng':30.52}

@app.route('/')
def homepage():
    return render_template('index.html',API_KEY = app.config['API_KEY'],center = Kyiv)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
