from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os.path


app = Flask(__name__)

def mkpath(p):
    return os.path.normpath(
        os.path.join(
            os.path.dirname(__file__),
            p))
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'sqlite:///' + mkpath('../cacapipi.db'))
app.url_map.strict_slashes = False

db = SQLAlchemy()
db.init_app(app)
