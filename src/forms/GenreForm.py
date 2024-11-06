from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField
from wtforms.validators import DataRequired
from hashlib import sha256
from .controllers import *
from models.Genre import Genre

class GenreForm(FlaskForm):
    id = HiddenField('id')
    nom_genre = StringField('Nom du genre', validators=[DataRequired()])
    def validate(self):
        if not FlaskForm.validate(self):
            return False
        if Genre.query.filter_by(nom_genre=self.nom_genre.data).first():
            self.nom_genre.errors('Ce genre existe déja')
            return False
        return True