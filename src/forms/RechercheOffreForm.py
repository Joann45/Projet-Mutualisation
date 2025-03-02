from collections.abc import Sequence
from typing import Any, Mapping
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, RadioField, SelectField, widgets,IntegerField
from wtforms.validators import DataRequired
from src.models.Reseau import Reseau
from src.models.Utilisateur import Utilisateur
from wtforms import SelectMultipleField, widgets
from markupsafe import Markup
 
 
class BootstrapListWidget(widgets.ListWidget):
 
    def __call__(self, field, **kwargs):
        kwargs.setdefault("id", field.id)
        html = [f"<{self.html_tag} {widgets.html_params(**kwargs)}>"]
        for subfield in field:
            if self.prefix_label:
                html.append(f"<li class='list-group-item'>{subfield.label} {subfield(class_='form-check-input ms-1')}</li>")
            else:
                html.append(f"<li class='list-group-item'>{subfield(class_='form-check-input me-1')} {subfield.label}</li>")
        html.append("</%s>" % self.html_tag)
        return Markup("".join(html))
 
 
class MultiCheckboxField(SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.
 
    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """
    widget = BootstrapListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()



class SelectRechercheOffreForm(FlaskForm):
    """Affichage des réseaux

    Args:
        FlaskForm (FlaskForm): FlaskForm
    """
    id = IntegerField(widget=HiddenField('id'))
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()
    reseaux = MultiCheckboxField('Reseaux')
    
class SelectDateProximité(FlaskForm):

    id = HiddenField("id")
    proxi = RadioField("Date d'expiration")

class SelectStatueOffre(FlaskForm):

    id = HiddenField("id")
    statue = RadioField("Status")



