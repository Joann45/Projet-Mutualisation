from .app import app
from flask import render_template, redirect, url_for, request

@app.route('/')
def connexion():
    """Renvoie la page de connexion

    Returns:
        connexion.html : Une page de connexion
    """
    return render_template('connexion.html')

@app.route('/mdp-oublie')
def mdp_oublie():
    """Renvoie la page du mot de passe oublié

    Returns:
        mdp-oublie.html : Une page demandant de rentrer son adresse mail pour réinitialiser le mot de passe
    """
    return render_template('mdp-oublie.html')

@app.route('/mdp-reset')
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
    return render_template('home.html')

@app.route('/home/les-offres')
def les_offres():
    """Renvoie la page des offres

    Returns:
        les-offres.html: Une page des offres
    """
    return render_template('les-offres.html')

@app.route('/home/profil')
def modifier_profil():
    """Renvoie la page de modification du profil

    Returns:
        profil.html: Une page de modification du profil
    """
    return render_template('profil.html')

@app.route('/home/mes-reseaux')
def mes_reseaux():
    """Renvoie la page des réseaux

    Returns:
        mes-reseaux.html: Une page des réseaux de l'utilisateur
    """
    return render_template('mes-reseaux.html')

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

@app.route('/home/visualiser-reponses-offres') ##!! A MODIFIER QUAND LA PAGE DE L'OFFRE SERA CREEE
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
    return render_template('mes-offres.html')

@app.route('/home/mes-offres/mes-reponses')

def mes_reponses():
    """Renvoie la page des réponses de l'utilisateur

    Returns:
        mes-reponses.html: Une page des réponses de l'utilisateur
    """
    return render_template('mes-reponses.html')

