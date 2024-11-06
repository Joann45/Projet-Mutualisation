from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, FileField, SelectField, DateField, FloatField, IntegerField
from wtforms.validators import DataRequired
from hashlib import sha256
from .controllers import *

class OffreForm(FlaskForm):
    id = HiddenField('id')
    nom_offre = StringField("Nom de l'offre", validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    date_limite = DateField("Date limite", validators=[DataRequired()])
    budget = FloatField("Budget", validators=[DataRequired()])
    cotisation_min = FloatField("Cotisation minimal", validators=[DataRequired()])
    capacite_min = IntegerField('Capacité minimal', validators=[DataRequired()])
    capacite_max = IntegerField('Capacité maximal', validators=[DataRequired()])
    img = FileField('Photo de profil', validators=[DataRequired()])
    etat = StringField("État de l'offre", validators=[DataRequired()])
    genre = SelectField('Genre', coerce=int)
    reseau = SelectField('Réseaux', coerce=int)
    nom_loc = StringField('Localisation', validators=[DataRequired()])
    date_deb = DateField('Date de début', validators=[DataRequired()])
    date_fin = DateField('Date de fin', validators=[DataRequired()])