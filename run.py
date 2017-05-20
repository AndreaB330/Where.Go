from app import *
import main
from flask_uploads import *

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, use_reloader=True)
