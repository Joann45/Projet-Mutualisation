from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, FileField, SelectField, DateField, FloatField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from datetime import date

class OffreForm(FlaskForm):
    id = HiddenField('id')
    nom_offre = StringField("Nom de l'offre", validators=[DataRequired()])
    description = TextAreaField('Description')
    date_limite = DateField("Date limite", validators=[DataRequired()])
    budget = FloatField("Budget Estimatif", validators=[DataRequired()])
    cotisation_min = FloatField("Cotisation minimal", validators=[DataRequired()])
    capacite_min = IntegerField('Capacité minimal', validators=[DataRequired()])
    capacite_max = IntegerField('Capacité maximal', validators=[DataRequired()])
    img = FileField("Image de l'offre")
    genre = SelectField('Genre', coerce=int)
    reseau = SelectField('Réseaux', coerce=int)
    etat = StringField('Etat')
    nom_loc = StringField('Localisation', validators=[DataRequired()])
    date_deb = DateField('Date de début', validators=[DataRequired()])
    date_fin = DateField('Date de fin', validators=[DataRequired()])
    liens = TextAreaField('Lien vers des ressources promotionnelles')
    documents = FileField("Ajouter les documents liés à l'offre")

    # def validate(self, extra_validators=None):
    #     if not FlaskForm.validate(self, extra_validators=extra_validators):
    #         return False

    #     # Validation de budget par rapport à la cotisation minimale
    #     if self.budget.data is not None and self.cotisation_min.data is not None:
    #         if self.cotisation_min.data > self.budget.data:
    #             self.budget.errors.append("Le budget doit être supérieur ou égal à la cotisation minimale.")
    #             return False

    #     # Validation de la capacité minimale par rapport à la capacité maximale
    #     if self.capacite_min.data is not None and self.capacite_max.data is not None:
    #         if self.capacite_min.data > self.capacite_max.data:
    #             self.capacite_min.errors.append("La capacité minimale doit être inférieure ou égale à la capacité maximale.")
    #             return False

    #     # Validation de la date limite par rapport à la date de début et aujourd'hui
    #     if self.date_limite.data is not None:
    #         if self.date_deb.data is not None and self.date_limite.data > self.date_deb.data:
    #             self.date_limite.errors.append("La date limite doit être antérieure ou égale à la date de début.")
    #             return False
    #         if self.date_limite.data < date.today():
    #             self.date_limite.errors.append("La date limite ne peut pas être dans le passé.")
    #             return False

    #     # Validation de la date de début par rapport à la date de fin
    #     if self.date_deb.data is not None and self.date_fin.data is not None:
    #         if self.date_deb.data > self.date_fin.data:
    #             self.date_deb.errors.append("La date de début doit être antérieure ou égale à la date de fin.")
    #             return False

    #     # Validation de la date de fin par rapport à la date de début
    #     if self.date_fin.data is not None:
    #         if self.date_deb.data is not None and self.date_fin.data < self.date_deb.data:
    #             self.date_fin.errors.append("La date de fin doit être postérieure ou égale à la date de début.")
    #             return False

    #     return True

class ReponseForm(FlaskForm):
    id = HiddenField('id')
    
    cotisation_apportee = FloatField("Cotisation apportée", validators=[DataRequired()])
    autre_rep = TextAreaField('Autres', validators=[DataRequired()])
    date_debut = DateField('Date de début', validators=[DataRequired()])
    date_fin = DateField('Date de fin', validators=[DataRequired()])
    cap_salle = IntegerField('Capacité de la salle', validators=[DataRequired()])
    submit = SubmitField("Repondre")
    
    def __init__(self, offre):
        super(ReponseForm, self).__init__()
        self.cotisation_min = offre.cotisation_min
        self.cotisation_apportee.render_kw = {'min': offre.cotisation_min, 'step': 0.01}
        self.date_debut.render_kw = {'min': offre.date_deb, 'max': offre.date_fin}
        self.date_fin.render_kw = {'min': offre.date_deb, 'max': offre.date_fin}
        self.cap_salle.render_kw = {'min': offre.capacite_min}

    def validate_cotisation_apportee(self, field):
        if field.data < self.cotisation_min:  # cotisation_min doit être défini dans votre formulaire
            raise ValidationError(f"La cotisation apportée ne peut pas être inférieure à {self.cotisation_min}.")
    
    #def validate(self, extra_validators = None):
    #    if not FlaskForm.validate(self, extra_validators = extra_validators):
    #        return False
    #    
    #    # Validation de la date de début par rapport à la date de fin
    #    if self.date_debut.data is not None and self.date_fin.data is not None:
    #        if self.date_debut.data > self.date_fin.data:
    #            self.date_debut.errors.append("La date de début doit être antérieure ou égale à la date de fin.")
    #            return False
    #    
    #    # Validation de la date de fin par rapport à la date de début
    #    if self.date_fin.data is not None:
    #        if self.date_debut.data is not None and self.date_fin.data < self.date_debut.data:
    #            self.date_fin.errors.append("La date de fin doit être postérieure ou égale à la date de début.")
    #            return False
    #    
    #    return True
    
class CommentaireForm(FlaskForm):
    id = HiddenField('id')
    texte_commentaire = TextAreaField('Commentaire', validators=[DataRequired()])
    submit = SubmitField("Commenter")