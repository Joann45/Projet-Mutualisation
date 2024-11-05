from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField
from wtforms.validators import DataRequired
from hashlib import sha256
from .controllers import *

class GenreForm(FlaskForm):
    id = HiddenField('id')
    nom_genre = StringField('Nom du genre', validators=[DataRequired()])