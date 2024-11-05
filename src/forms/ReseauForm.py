from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField
from wtforms.validators import DataRequired
from hashlib import sha256
from .controllers import *

class ReseauForm(FlaskForm):
    id = HiddenField('id')
    nom_reseau = StringField('Nom du réseau', validators=[DataRequired()])