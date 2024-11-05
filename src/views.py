from .app import app
from flask import render_template, redirect, url_for, request

@app.route('/')
def connexion():
    return render_template('connexion.html')

@app.route('/mdp-oublie')
def mdp_oublie():
    return render_template('mdp-oublie.html')

@app.route('/mdp-reset')
def mdp_reset():
    return render_template('mdp-reset.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/home/les-offres')
def les_offres():
    return render_template('les-offres.html')

@app.route('/home/profil')
def modifier_profil():
    return render_template('profil.html')

@app.route('/home/mes-reseaux')
def mes_reseaux():
    return render_template('mes-reseaux.html')

@app.route('/home/mes-reseaux-admin')
def gerer_mes_reseaux():
    return render_template('mes-reseaux-admin.html')

@app.route('/home/creation-offre')
def creation_offre():
    return render_template('creation-offre.html')

@app.route('/home/visualiser-reponses-offres') ##!! A MODIFIER QUAND LA PAGE DE L'OFFRE SERA CREEE
def visualiser_offre():
    return render_template('visualiser-reponses-offres.html')
