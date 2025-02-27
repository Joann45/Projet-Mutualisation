from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_security import login_required, current_user, roles_required,  logout_user, login_user
from src.forms.UtilisateurForm import InscriptionForm, ConnexionForm, UpdateUser, UpdatePassword
from src.forms.MotDePasseForm import ResetPasswordForm, SendMailResetForm
import os
from hashlib import sha256
from src.models import Notification, Notification_Utilisateur
from src.models.Utilisateur import Utilisateur
from src.models.Reseau import Reseau
from src.models.Role import Role, roles
from src.extensions import db, login_manager
from src.reseaux.reseaux import send_email_with_timeout


auth_bp = Blueprint('auth', __name__, template_folder='templates')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Renvoie la page de connexion

    Returns:
        connexion.html : Une page de connexion
    """
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    f = ConnexionForm()
    if f.validate_on_submit():
        u = f.get_authenticated_user()
        if u:
            login_user(u)
            return redirect(url_for('views.home'))
    return render_template('auth/connexion.html', form=f)

@auth_bp.route('/signin', methods=['GET','POST'])
def signin():
    f = InscriptionForm()
    f.role.choices =[(role.id_role, role.name) for role in Role.query.all()]
    if f.validate_on_submit():
        u = Utilisateur()
        u.nom_utilisateur = f.nom_user.data
        u.prenom_utilisateur = f.prenom_user.data
        u.mdp_utilisateur = sha256(f.mot_de_passe.data.encode()).hexdigest()
        u.email_utilisateur = f.email.data
        u.img_utilisateur = str(Utilisateur.get_last_id()+1)
        u.role_id = f.role.data
        file = f.img.data
        if file:
            if not os.path.exists("src/static/img/profil"):
                os.makedirs("src/static/img/profil")
            file.save(os.path.join("src/static/img/profil", str(Utilisateur.get_last_id()+1)))
        
        db.session.add(u)
        db.session.commit()

        mail_dest_utilisateur = u.email_utilisateur
        notification = Notification(
            type_operation="bienvenue", 
            date_notification=datetime.now(), 
            heure_notification=datetime.now().replace(microsecond=0).time(), 
            expediteur="StageFlow",
        )
        db.session.add(notification)
        db.session.flush() 

        notification_utilisateur = Notification_Utilisateur(
            id_utilisateur=u.id_utilisateur,
            id_notif=notification.id_notif  
        )
        
        db.session.add(notification_utilisateur)
        db.session.commit()
        try : 
            send_email_with_timeout(
                mail_dest_utilisateur,
                "Invitation pour StageFlow",
                "Vous avez été invité à StageFlow.",
                f"<b>Vous avez été invité à rejoindre la communauté de StageFlow</b> <br> Votre identifiant : {mail_dest_utilisateur}<br> <p>Voici votre mot de passe : {f.mot_de_passe.data}</p> <br><a href='http://127.0.0.1:5000/auth/login'>Cliquez ici</a>"
            )
        except Exception as e:
            print(f"❌ Erreur lors de l'envoi de l'e-mail: {e}")
        return redirect(url_for('auth.login'))
    return render_template('auth/signin.html', form=f)

@auth_bp.route('/logout')
@login_required
def logout():
    """Déconnecte l'utilisateur

    Returns:
        login : Redirige vers la page de connexion
    """
    logout_user()
    return redirect(url_for('auth.login'))

@auth_bp.route('/mdp-oublie',methods=['GET','POST'])
def mdp_oublie():
    """Renvoie la page du mot de passe oublié

    Returns:
        mdp-oublie.html : Une page demandant de rentrer son adresse mail pour réinitialiser le mot de passe
    """
    f = SendMailResetForm()
    if f.validate_on_submit():
        mail_dest_utilisateur = f.adress_mail.data
        lien = f"http://127.0.0.1:5000/auth/mdp-reset/{mail_dest_utilisateur}"
        email_body = f"<b>Cliquez sur le lien pour réinitialiser votre mot de passe</b> <br> <a href='{lien}'> Réinitialiser votre mot de passe </a>"
        send_email_with_timeout(mail_dest_utilisateur, "Réinitialisation du mot de passe", "Réinitialisation de votre mot de passe", email_body)
    return render_template('auth/mdp-oublie.html',form= f)

@auth_bp.route('/mdp-reset/<string:email>', methods=['GET', 'POST'])
def mdp_reset(email):
    """Renvoie la page de réinitialisation du mot de passe

    Returns:
        mdp-reset.html: Une page pour réinitialiser le mot de passe
    """
    f = ResetPasswordForm()

    # L'email est directement passé dans l'URL, pas besoin de request.args
    if not email:
        return redirect(url_for('auth.mdp_oublie'))
   
    f.adress_mail.data = str(email) 
    print(type(f.adress_mail.data), f.adress_mail.data)

    if f.validate_on_submit():
        user = Utilisateur.query.filter_by(email_utilisateur=email).first()
        if user:
            user.mdp_utilisateur = sha256(f.new_password.data.encode()).hexdigest()
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            flash("Utilisateur introuvable.", "error")
            return redirect(url_for('auth.mdp_oublie'))
    
    return render_template('auth/mdp-reset.html', form=f,email=email)


@auth_bp.route('/mdp-modif', methods=['GET','POST'])
@login_required
@roles("Administrateur", "Organisateur")
def mdp_modif():
    f = UpdatePassword()
    if f.validate_on_submit():
        if f.validate():
            user = current_user
            user.mdp_utilisateur = sha256(f.new_password.data.encode()).hexdigest()
            db.session.commit()
            return redirect(url_for('views.home'))
    return render_template('mdp-modif.html', form = f)

