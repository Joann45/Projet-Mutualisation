import os.path
from flask_mail import Mail, Message
from flask import Flask, render_template

mail = Mail()
    

def mkpath(p):
    return os.path.normpath(
        os.path.join(
            os.path.dirname(__file__),
            p))

def init_app(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        'sqlite:///' + mkpath('../testdb.db'))
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_size': 10,
        'max_overflow': 20,
        'pool_recycle': 1800,
        'pool_pre_ping': True,
    }
    app.url_map.strict_slashes = False
    app.config['SECRET_KEY'] = 'e9767196-4490-415a-8d42-1b16d2ad2a24'
    app.config['SECURITY_DEFAULT_REMEMBER_ME'] = False
    app.config['SECURITY_REGISTERABLE'] = False
    app.config['SECURITY_RECOVERABLE'] = False
    app.config['SECURITY_TRACKABLE'] = False
    app.config['SECURITY_CONFIRMABLE'] = False
    app.config['SECURITY_CHANGEABLE'] = False
    app.config['BOOTSTRAP_SERVE_LOCAL'] = True
    app.config['SECURITY_LOGIN_URL'] = '/auth/login'
  

    # Configuration du serveur SMTP
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465  # Pour SSL (recommandé) OU 587 pour TLS
    app.config['MAIL_USE_TLS'] = False  # Désactiver TLS si SSL est utilisé
    app.config['MAIL_USE_SSL'] = True   # Activer SSL

    app.config['MAIL_USERNAME'] = 'stageflow45@gmail.com'  # Adresse email
    app.config['MAIL_PASSWORD'] = 'cpeo uxwo lajr wwqd'  # Mot de passe (Note: Pour Gmail vous aurez besoin d'un mot de passe d'application)
    app.config['MAIL_DEFAULT_SENDER'] = 'stageflow45@gmail.com'  # Expéditeur par défaut
    mail.init_app(app)

  
