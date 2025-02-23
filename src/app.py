from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required
from flask_bootstrap import Bootstrap5
from src.extensions import db, login_manager
from src.auth.auth import auth_bp
from flask_security import Security, SQLAlchemySessionUserDatastore
from src.models.Utilisateur import Utilisateur
from src.models.Offre import Offre
from src.models.Role import Role, roles
from flask import render_template

app = Flask(__name__)

import src.config as config

db.init_app(app)

# Route de app
@app.route('/home', methods=['GET','POST'])
@app.route('/', methods=['GET','POST'])
@login_required
@roles("Administrateur","Organisateur") #! A modifier pour les rôles
def home():
    """Renvoie la page d'accueil

    Returns:
        home.html: Une page d'accueil
    """
    les_offres = Offre.query.all()[:3] #! A modifier plus tard pour trier par les plus populaires
    return render_template('home.html', offres=les_offres)

login_manager.init_app(app)

login_manager.login_view = 'auth.login'

bootstrap = Bootstrap5(app)
# @login_manager.user_loader
# def load_user(user_id):
#     return Utilisateur.query.get(int(user_id))

# Import des routes

app.register_blueprint(auth_bp, url_prefix='/auth')
user_datastore = SQLAlchemySessionUserDatastore(db.session, Utilisateur, Role)
security = Security(app, user_datastore)


