from .app import app
from flask import render_template, redirect, url_for, request

@app.route('/')
def index():
    return render_template('base.html')


@app.route('/profil')
def modifier_profil():
    return render_template('profil.html')