from .app import app
from flask import render_template, redirect, url_for, request

@app.route('/')
def index():
    return render_template('base.html')


@app.route('/profil')
def modifier_profil():
    return render_template('profil.html')

@app.route('/mes_reseaux')
def voir_mes_reseaux():
    return render_template('voir_mes_reseaux.html')

@app.route('/mes_reseaux_admin')
def gerer_mes_reseaux():
    return render_template('gerer_mes_reseaux.html')

