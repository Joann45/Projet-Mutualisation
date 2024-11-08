from collections.abc import Sequence
from typing import Any, Mapping
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, RadioField, SelectField
from wtforms.validators import DataRequired
from src.models.Reseau import Reseau
from src.models.Utilisateur import Utilisateur

class ReseauForm(FlaskForm):
    id = HiddenField('id')
    nom_reseau = StringField('Nom du réseau', validators=[DataRequired()])
    def validate(self, extra_validators=None):
        if not FlaskForm.validate(self):
            return False
        if Reseau.query.filter_by(nom_reseau=self.nom_reseau.data).first():
            self.nom_reseau.errors.append('Un réseau existe déjà avec ce nom')
            return False
        return True

class AddUtilisateurReseauForm(FlaskForm):
    id = HiddenField('id')
    utilisateur = SelectField('Utilisateur', validators=[DataRequired()])

class SelectReseauForm(FlaskForm):
    id = HiddenField('id')
    reseaux = RadioField('Réseaux', validators=[DataRequired()])
