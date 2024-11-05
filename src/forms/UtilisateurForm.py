from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, FileField, PasswordField
from wtforms.validators import DataRequired
from hashlib import sha256
from .controllers import *

class UtilisateurForm(FlaskForm):
    id = HiddenField('id')
    nom_user = StringField('Nom', validators=[DataRequired()])
    prenom_user = StringField('Prenom', validators=[DataRequired()])
    mot_de_passe = PasswordField('Mot de passe', validators=[DataRequired()])
    email = StringField('Adresse mail', validators=[DataRequired()])
    img = FileField('Photo de profil', validators=[DataRequired()])
