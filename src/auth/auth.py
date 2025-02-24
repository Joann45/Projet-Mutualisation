from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_security import login_required, current_user, roles_required,  logout_user, login_user
from src.forms.UtilisateurForm import InscriptionForm, ConnexionForm, UpdateUser, UpdatePassword
import os
from hashlib import sha256
from src.models.Utilisateur import Utilisateur
from src.models.Reseau import Reseau
from src.models.Role import Role, roles
from src.extensions import db, login_manager


auth_bp = Blueprint('auth', __name__, template_folder='templates')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Renvoie la page de connexion

    Returns:
        connexion.html : Une page de connexion
    """
    if current_user.is_authenticated:
        return redirect(url_for('home'))
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
        if f.validate():
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

@auth_bp.route('/mdp-oublie') # TODO : A faire -> le form et les interactions avec la base de données
def mdp_oublie():
    """Renvoie la page du mot de passe oublié

    Returns:
        mdp-oublie.html : Une page demandant de rentrer son adresse mail pour réinitialiser le mot de passe
    """
    return render_template('auth/mdp-oublie.html')

@auth_bp.route('/mdp-reset') # TODO : A faire -> le form et les interactions avec la base de données
def mdp_reset():
    """Renvoie la page de réinitialisation du mot de passe

    Returns:
        mdp-reset.html: Une page pour réinitialiser le mot de passe
    """
    return render_template('auth/templates/mdp-reset.html')

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
    return render_template('auth/templates/mdp-modif.html', form = f)