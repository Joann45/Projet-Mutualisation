from .app import app, db
from flask import render_template, redirect, url_for, request
from flask_security import login_required, current_user, roles_required,  logout_user, login_user
from src.forms.UtilisateurForm import InscriptionForm, ConnexionForm
from src.models.Utilisateur import Utilisateur
from src.models.Reseau import Reseau
from src.models.Role import Role
from src.models.Offre import Offre
from hashlib import sha256
from flask_security import Security, SQLAlchemySessionUserDatastore
from src.forms.ReseauForm import SelectReseauForm
import os


@app.route('/')
@app.route('/login', methods=['GET','POST'])
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
            return redirect(url_for('home'))
    return render_template('connexion.html', form=f)

@app.route('/signin', methods=['GET','POST'])
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
            u.img_utilisateur = f.img.data.filename
            u.role_id = f.role.data
            file = f.img.data
            if file:
                file.save(os.path.join("src/static/img/profil", file.filename))
            db.session.add(u)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('signin.html', form=f)

@app.route('/logout')
@login_required
def logout():
    """Déconnecte l'utilisateur

    Returns:
        login : Redirige vers la page de connexion
    """
    logout_user()
    return redirect(url_for('login'))


# A charger après la définition de la route login
user_datastore = SQLAlchemySessionUserDatastore(db.session, Utilisateur, Role)
security = Security(app, user_datastore)


@app.route('/mdp-oublie') # TODO : A faire -> le form et les interactions avec la base de données
def mdp_oublie():
    """Renvoie la page du mot de passe oublié

    Returns:
        mdp-oublie.html : Une page demandant de rentrer son adresse mail pour réinitialiser le mot de passe
    """
    return render_template('mdp-oublie.html')

@app.route('/mdp-reset') # TODO : A faire -> le form et les interactions avec la base de données
def mdp_reset():
    """Renvoie la page de réinitialisation du mot de passe

    Returns:
        mdp-reset.html: Une page pour réinitialiser le mot de passe
    """
    return render_template('mdp-reset.html')

@app.route('/home')
def home():
    """Renvoie la page d'accueil

    Returns:
        home.html: Une page d'accueil
    """
    les_offres = Offre.query.all()[:3] #! A modifier plus tard pour trier par les plus populaires
    return render_template('home.html', offres=les_offres)

@app.route('/home/les-offres')
def les_offres():
    """Renvoie la page des offres

    Returns:
        les-offres.html: Une page des offres
    """
    les_offres = Offre.query.all()
    return render_template('les-offres.html', offres=les_offres)

@app.route('/home/repondre_offre/<int:id_offre>')
def repondre_offre(id_offre):
    o = Offre.query.get(id_offre)
    if not o:
        return redirect(url_for("home"))
    return render_template('repondre-offre.html', offre=o)

@app.route('/home/profil')
def modifier_profil():
    """Renvoie la page de modification du profil

    Returns:
        profil.html: Une page de modification du profil
    """
    u = Utilisateur.query.get(current_user.id_utilisateur)
    return render_template('profil.html', user=u) #! A modifier pour afficher les informations de l'utilisateur

@app.route('/home/mes-reseaux')
def mes_reseaux():
    """Renvoie la page des réseaux

    Returns:
        mes-reseaux.html: Une page des réseaux de l'utilisateur
    """
    f = SelectReseauForm()
    f.reseaux.choices = [(reseau.id_reseau, reseau.nom_reseau) for reseau in Reseau.query.all()]
    return render_template('mes-reseaux.html', form=f)

@app.route('/home/mes-reseaux-admin')
def mes_reseaux_admin():
    """Renvoie la page des réseaux administrateur

    Returns:
        mes-reseaux-admin.html: Une page des réseaux pour un organisateur
    """
    return render_template('mes-reseaux-admin.html')

@app.route('/home/creation-offre')
def creation_offre():
    """Renvoie la page de création d'une offre

    Returns:
        creation-offre.html: Une page de création d'une offre
    """
    return render_template('creation-offre.html')

@app.route('/home/visualiser-reponses-offres') #! A MODIFIER QUAND LA PAGE DE L'OFFRE SERA CREEE
def visualiser_offre():
    """Renvoie la page de visualisation des réponses aux offres

    Returns:
        visualiser-reponses-offres.html: Une page de visualisation des réponses aux offres
    """
    return render_template('visualiser-reponses-offres.html')

@app.route('/home/mes-offres')
def mes_offres():
    """Renvoie la page des offres de l'utilisateur

    Returns:
        mes-offres.html: Une page des offres de l'utilisateur
    """
    les_offres = Offre.query.filter_by(id_utilisateur=current_user.id_utilisateur).all()
    return render_template('mes-offres.html', offres=les_offres)

@app.route('/home/mes-offres/mes-reponses')

def mes_reponses():
    """Renvoie la page des réponses de l'utilisateur

    Returns:
        mes-reponses.html: Une page des réponses de l'utilisateur
    """
    return render_template('mes-reponses.html')
