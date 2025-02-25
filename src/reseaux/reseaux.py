from src.extensions import db
from flask import render_template, redirect, url_for, request
from flask_security import login_required, current_user, roles_required,  logout_user, login_user
from src.forms.UtilisateurForm import InscriptionForm, ConnexionForm, UpdateUser, UpdatePassword
from flask import render_template, redirect, url_for, request, send_from_directory, Blueprint
from src.forms.UtilisateurForm import InscriptionForm, ConnexionForm
from src.forms.OffreForm import OffreForm, ReponseForm, CommentaireForm
from src.forms.GenreForm import GenreForm
from src.models import Notification, Notification_Utilisateur
from src.models.Utilisateur import Utilisateur
from src.models.Reseau import Reseau
from src.models.Role import Role
from src.models.Offre import Offre
from src.models.Genre import Genre
from src.models.Reponse import Reponse
from src.models.Document import Document
from src.models.Genre_Offre import Genre_Offre
from src.models.Offre_Reseau import Offre_Reseau
from src.models.Utilisateur_Reseau import Utilisateur_Reseau
from src.models.Commentaire import Commentaire
from src.forms.ReseauForm import ReseauForm, AddUtilisateurReseauForm
from datetime import datetime
from hashlib import sha256
from flask_security import Security, SQLAlchemySessionUserDatastore
from src.forms.ReseauForm import SelectReseauForm
from src.forms.RechercheOffreForm import SelectRechercheOffreForm, SelectDateProximité
from werkzeug.utils import secure_filename
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import os
from functools import wraps
from flask import abort
from flask_mail import Message, Mail
from src.config import mail
from flask import render_template, current_app
from flask_mail import Message
import socket
socket.setdefaulttimeout(3)

reseaux_bp = Blueprint('reseaux', __name__, template_folder='templates')

@reseaux_bp.route('/home/mes-reseaux', methods=['GET', 'POST'])
def mes_reseaux():
    """Affiche la page des réseaux."""
    f_select_reseau = SelectReseauForm()
    add_user_form = AddUtilisateurReseauForm()
    add_form = ReseauForm()
    les_reseaux = get_reseaux_for_user(current_user)
    
    if not les_reseaux:
        if not current_user.is_admin():
            return render_template('pas_reseau.html')
        return render_template('mes-reseaux-admin.html', reseaux=[], add_form=add_form, select_form=None, membres=[])

    # Déterminer le réseau sélectionné
    reseau_id = request.args.get('reseau_id', type=int) or les_reseaux[0].id_reseau
    # Préparer le formulaire de sélection
    f_select_reseau.reseaux.choices = [(r.id_reseau, r.nom_reseau) for r in les_reseaux]
    f_select_reseau.reseaux.default = reseau_id
    f_select_reseau.process()

    # Récupérer le réseau sélectionné et définir le formulaire d'ajout d'utilisateur
    reseau = Reseau.query.get(reseau_id)
    add_user_form.utilisateur.choices = get_available_users_for_reseau(reseau)

    # Récupérer les offres associées
    les_offres = Offre.query.filter(Offre.les_reseaux.any(id_reseau=reseau_id)).all()

    return render_template(
        'mes-reseaux-admin.html',
        add_user_form=add_user_form,
        add_form=add_form,
        reseaux=les_reseaux,
        select_form=f_select_reseau,
        membres=[[membre.orga for membre in reseau.les_utilisateurs]],
        reseau_id=reseau_id,
        offres=les_offres,
        reseau=reseau
    )
    
# Route pour traiter la soumission du formulaire de sélection de réseau
@reseaux_bp.route('/home/mes-reseaux/select', methods=['POST'])
def select_reseau():
    f_select_reseau = SelectReseauForm()
    if f_select_reseau.validate_on_submit():
        reseau_id = f_select_reseau.reseaux.data
        return redirect(url_for('reseaux.mes_reseaux', reseau_id=reseau_id))
    # En cas d'erreur, retourne à la page principale
    return redirect(url_for('reseaux.mes_reseaux'))

# Route pour traiter la création d'un nouveau réseau
@reseaux_bp.route('/home/mes-reseaux/ajout', methods=['POST'])
def ajout_reseau():
    f_add_reseau = ReseauForm()
    if f_add_reseau.validate_on_submit():
        print("Ajout du réseau")
        add_new_reseau(f_add_reseau)
    return redirect(url_for('reseaux.mes_reseaux'))

def get_reseaux_for_user(user):
    """Récupère les réseaux en fonction du rôle de l'utilisateur."""
    if user.is_admin():
        return Reseau.query.all()
    return Reseau.query.filter(Reseau.les_utilisateurs.any(id_utilisateur=user.id_utilisateur)).all()

def get_available_users_for_reseau(reseau):
    """Récupère les utilisateurs disponibles pour être ajoutés au réseau."""
    liste_utilisateurs = [utilisateur.id_utilisateur for utilisateur in reseau.les_utilisateurs]
    return [(utilisateur.id_utilisateur, utilisateur.nom_utilisateur) for utilisateur in Utilisateur.query.all() if utilisateur.id_utilisateur not in liste_utilisateurs]

def add_new_reseau(form):
    """Ajoute un nouveau réseau à la base de données."""
    r = Reseau()
    r.nom_reseau = form.nom_reseau.data
    db.session.add(r)
    db.session.commit()

@reseaux_bp.route('/home/suppression_reseau/<int:id_reseau>', methods=['GET'])
def suppression_reseau(id_reseau):
    """Supprime un réseau
    Args:
        id_reseau (int): L'identifiant du réseau
    Returns:
        mes-reseaux-admin.html: Une page des réseaux pour un organisateur
    """
    reseau = Reseau.query.get(id_reseau)
    if reseau:
        db.session.delete(reseau)
        db.session.commit()
    return redirect(url_for('reseaux.mes_reseaux'))


@reseaux_bp.route('/home/mes-reseaux-admin/suppression_utilisateur/<int:id_reseau>/<int:id_utilisateur>', methods=['GET', 'POST'])
def suppression_utilisateur_reseau(id_reseau, id_utilisateur):
    """Supprime un utilisateur d'un réseau
    Args:
        id_reseau (int): L'identifiant du réseau
        id_utilisateur (int): L'identifiant de l'utilisateur à supprimer
    Returns:
        mes-reseaux-admin.html: Une page des réseaux pour un organisateur
    """
    utilisateur_reseau = Utilisateur_Reseau.query.filter_by(id_reseau=id_reseau, id_utilisateur=id_utilisateur).first()
    if utilisateur_reseau:
        db.session.delete(utilisateur_reseau)
        db.session.commit()
    return redirect(url_for('reseaux.mes_reseaux', reseau_id=id_reseau))


from flask import flash

def send_email_with_timeout(mail_dest_utilisateur, subject, body, html):
    try:
        msg = Message(subject,
                      sender=current_app.config['MAIL_DEFAULT_SENDER'],
                      recipients=[mail_dest_utilisateur])
        msg.body = body
        msg.html = html
        mail.send(msg)
        print("✅ E-mail envoyé avec succès !")


    except socket.timeout:
        print("❌ Timeout dépassé pour l'envoi de l'email")
        flash("L'utilisateur a été ajouté, mais l'e-mail n'a pas pu être envoyé dans le délai imparti.", "warning")
    except Exception as e:
        print(f"❌ Erreur lors de l'envoi de l'e-mail: {e}")
        flash("L'utilisateur a été ajouté, mais l'e-mail n'a pas pu être envoyé.", "warning")

@reseaux_bp.route('/home/mes-reseaux-admin/ajout_utilisateur/<int:id_reseau>', methods=['GET', 'POST'])
def ajout_utilisateur_reseau(id_reseau):
    """Ajoute un utilisateur à un réseau
    Args:
        id_reseau (int): L'identifiant du réseau
    Returns:
        mes-reseaux-admin.html: Une page des réseaux pour un organisateur
    """
    reseau = Reseau.query.get(id_reseau)
    if not reseau:
        return redirect(url_for('reseaux.mes_reseaux'))

    form = AddUtilisateurReseauForm()
    liste_utilisateurs = [utilisateur.id_utilisateur for utilisateur in reseau.les_utilisateurs]
    form.utilisateur.choices = [(utilisateur.id_utilisateur, utilisateur.nom_utilisateur) 
                                for utilisateur in Utilisateur.query.all() 
                                if utilisateur.id_utilisateur not in liste_utilisateurs]
    
    if form.validate_on_submit():
        utilisateur_id = form.utilisateur.data
        utilisateur_reseau = Utilisateur_Reseau(id_reseau=id_reseau, id_utilisateur=utilisateur_id)
        db.session.add(utilisateur_reseau)
        notification = Notification(type_operation="Ajout d'un utilisateur à un réseau", date_notification=datetime.now())
        db.session.add(notification)
        db.session.commit()

        try:
            mail_dest_utilisateur = Utilisateur.query.filter_by(id_utilisateur=utilisateur_id).first().email_utilisateur
            send_email_with_timeout(mail_dest_utilisateur, "Ajout à un réseau", "Vous avez été ajouté à un réseau.", "<b>Vous avez été ajouté à un réseau.</b>")
    
           
        except Exception as e:
            print(f"❌ Erreur lors de l'envoi de l'e-mail: {e}")
            flash("L'utilisateur a été ajouté, mais l'e-mail n'a pas pu être envoyé.", "warning")

        return redirect(url_for('reseaux.mes_reseaux', reseau_id=id_reseau))

    return render_template('add-utilisateur-reseau.html', form=form, reseau=reseau)
