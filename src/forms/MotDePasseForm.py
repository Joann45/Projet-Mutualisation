from flask_wtf import FlaskForm
from flask_security import current_user
from wtforms import StringField, HiddenField, FileField, PasswordField, RadioField
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
    def validate(self, extra_validators=None):
        if not super().validate(extra_validators=extra_validators):
            return False
        if self.confirm_password.data != self.new_password.data:
            self.new_password.errors.append("Le nouveau mot de passe ne correspond pas à la confirmation")
            return False
        if self.current_password.data == self.new_password.data:
            self.new_password.errors.append("Le nouveau mot de passe est le même le l'ancien")
            return False
        return True
        
class SendMailResetForm(FlaskForm):
    id = HiddenField('id')
    adress_mail =  StringField('Adresse e-mail', validators=[DataRequired()])
    
            
        
        