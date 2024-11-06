from .app import app, db
from flask import render_template, redirect, url_for, request
from flask_security import login_required, current_user, roles_required,  logout_user, login_user
from src.forms.UtilisateurForm import InscriptionForm, ConnexionForm
from src.models.Utilisateur import Utilisateur
from src.models.Role import Role
from hashlib import sha256
from flask_security import Security, SQLAlchemySessionUserDatastore


@app.route('/')
def index():
    return render_template('index.html')

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
            u.img_utilisateur = f.img.data
            u.role_id = f.role.data
            db.session.add(u)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('signin.html', form=f)


@app.route('/login', methods=['GET','POST'])
def login():
    f = ConnexionForm()
    if f.validate_on_submit():
        u = f.get_authenticated_user()
        if u:
            login_user(u)
            return redirect(url_for('index'))
    return render_template('login.html', form=f)


# A charger après la définition de la route login
user_datastore = SQLAlchemySessionUserDatastore(db.session, Utilisateur, Role)
security = Security(app, user_datastore)