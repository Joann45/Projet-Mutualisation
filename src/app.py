from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap5
from src.extensions import db, login_manager
from src.auth.auth import auth_bp
from src.reseaux.reseaux import reseaux_bp
from src.reponse_offre.reponse_offre import reponse_bp
from src.views import views_bp
from flask_security import Security, SQLAlchemySessionUserDatastore
from src.models.Utilisateur import Utilisateur
from src.models.Role import Role
from flask import render_template
import uuid
import src.config as config

login_manager = LoginManager()

def create_app(config_object='src.config'):
    app = Flask(__name__)
    
    config.init_app(app)
    
    # Initialiser les extensions
    db.init_app(app)
    login_manager.init_app(app)
    Bootstrap5(app)
    
    # Enregistrer les Blueprints
    app.register_blueprint(reseaux_bp)
    app.register_blueprint(reponse_bp)
    app.register_blueprint(views_bp)

    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    user_datastore = SQLAlchemySessionUserDatastore(db.session, Utilisateur, Role)
    security = Security(app, user_datastore)

    login_manager.login_view = 'auth.login'
    login_manager.login_url = "/auth/login"

    return app

@login_manager.user_loader
def load_user(user_id):
    if not user_id:
        return None
    try:
        if isinstance(user_id, uuid.UUID):
            user_id = str(user_id)
        return Utilisateur.query.filter_by(fs_uniquifier=user_id).first()
    except Exception as e:
        print(f"Erreur: {e}")
        return None



