from flask_wtf import FlaskForm
from flask_security import current_user
from wtforms import StringField, HiddenField, FileField, PasswordField, RadioField, SubmitField
from wtforms.validators import DataRequired
from hashlib import sha256
from src.models.Role import Role
from src.models.Utilisateur import Utilisateur
from flask import current_app

class ResetPasswordForm(FlaskForm):
    id = HiddenField('id')
    adress_mail = StringField('Adresse e-mail', validators=[DataRequired()])
    new_password = PasswordField('Nouveau mot de passe', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmation mot de passe', validators=[DataRequired()])
    def validate(self, extra_validators = None):
        return True
    
        
class SendMailResetForm(FlaskForm):
    adress_mail = StringField("Adresse e-mail", validators=[DataRequired()])
    submit = SubmitField("Envoyer un mail de réinitialisation")

        
        