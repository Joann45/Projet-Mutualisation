from collections.abc import Sequence
from typing import Any, Mapping
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField
from wtforms.validators import DataRequired
from src.models.Reseau import Reseau
from src.models.Utilisateur import Utilisateur

class ReseauForm(FlaskForm):
    id = HiddenField('id')
    nom_reseau = StringField('Nom du réseau', validators=[DataRequired()])
    def validate(self):
        if not FlaskForm.validate(self):
            return False
        if Reseau.query.filter_by(nom_reseau=self.nom_reseau.data).first():
            self.nom_reseau.errors.append('Un réseau existe déjà avec ce nom')
            return False
        return True

class AddUtilisateurReseauForm(FlaskForm):
    id = HiddenField('id')
    reseau = StringField('Réseau', validators=[DataRequired()])
    email_utilisateur = StringField('Email utilisateur', validators=[DataRequired()])
    def validate(self):
        if not FlaskForm.validate(self):
            return False
        if not Reseau.query.filter_by(nom_reseau=self.reseau.data).first():
            self.reseau.errors.append('Ce réseau n\'existe pas')
            return False
        if not Utilisateur.query.filter_by(email_utilisateur=self.email_utilisateur.data).first():
            self.email_utilisateur.errors.append('Cet utilisateur n\'existe pas')
            return False
        return True
