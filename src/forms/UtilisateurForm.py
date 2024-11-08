from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, FileField, PasswordField, RadioField
from wtforms.validators import DataRequired
from hashlib import sha256
from src.models.Role import Role
from src.models.Utilisateur import Utilisateur
from flask import current_app


class InscriptionForm(FlaskForm):
    id = HiddenField('id')
    nom_user = StringField('Nom', validators=[DataRequired()])
    prenom_user = StringField('Prenom', validators=[DataRequired()])
    mot_de_passe = PasswordField('Mot de passe', validators=[DataRequired()])
    confirmation_mot_de_passe = PasswordField('Confirmation mot de passe', validators=[DataRequired()])
    email = StringField('Adresse mail', validators=[DataRequired()])
    img = FileField('Photo de profil', validators=[DataRequired()])
    role = RadioField('Role', validators=[DataRequired()])
    def validate(self, extra_validators=None):
        if not FlaskForm.validate(self, extra_validators=extra_validators):
            return False
        if self.mot_de_passe.data != self.confirmation_mot_de_passe.data:
            self.confirmation_mot_de_passe.errors.append('Les mots de passe ne correspondent pas')
            return False
        if Utilisateur.query.filter_by(email_utilisateur=self.email.data).first():
            self.email.errors.append('Un utilisateur existe déjà avec cette adresse mail')
            return False
        return True

class ConnexionForm(FlaskForm):
    id=HiddenField('id')
    email=StringField('Adresse mail', validators=[DataRequired()])
    mot_de_passe=PasswordField('Mot de passe', validators=[DataRequired()])
    def get_authenticated_user(self):
        u = Utilisateur.query.filter_by(email_utilisateur=self.email.data).first()
        if u and u.mdp_utilisateur == sha256(self.mot_de_passe.data.encode()).hexdigest():
            return u
        return None