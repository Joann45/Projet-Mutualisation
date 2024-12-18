from .app import app, db
from flask import render_template, redirect, url_for, request
from flask_security import login_required, current_user, roles_required,  logout_user, login_user
from src.forms.UtilisateurForm import InscriptionForm, ConnexionForm, UpdateUser, UpdatePassword
from flask import render_template, redirect, url_for, request
from src.forms.UtilisateurForm import InscriptionForm, ConnexionForm
from src.forms.OffreForm import OffreForm, ReponseForm
from src.forms.GenreForm import GenreForm
from src.models.Utilisateur import Utilisateur
from src.models.Reseau import Reseau
from src.models.Role import Role
from src.models.Offre import Offre
from src.models.Genre import Genre
from src.models.Reponse import Reponse
from src.models.Document import Document
from src.models.Genre_Offre import Genre_Offre
from src.models.Offre_Reseau import Offre_Reseau
from src.models.Utilisateur_Reseau import Utilisateur_Reseau
from src.forms.ReseauForm import ReseauForm, AddUtilisateurReseauForm
from hashlib import sha256
from flask_security import Security, SQLAlchemySessionUserDatastore
from src.forms.ReseauForm import SelectReseauForm
import os
from functools import wraps
from flask import abort

def roles(*roles):
    """Vérifie si l'utilisateur a un rôle parmi ceux passés en paramètre
    
    Args:
        *roles : Les rôles à vérifier
        
    Returns:
        decorator : La fonction décorée
    Examples:
        >>> @roles("Administrateur","Organisateur")
        >>> def home():
        >>>     return render_template('home.html')
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not Role.query.get(current_user.role_id).name in roles:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

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
            u.img_utilisateur = str(Utilisateur.get_last_id())
            u.role_id = f.role.data
            file = f.img.data
            if file:
                file.save(os.path.join("src/static/img/profil", str(Utilisateur.get_last_id())))
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

@app.route('/mdp-modif', methods=['GET','POST'])
@login_required
@roles("Administrateur", "Organisateur")
def mdp_modif():
    f = UpdatePassword()
    if f.validate_on_submit():
        if f.validate():
            user = current_user
            user.mdp_utilisateur = sha256(f.new_password.data.encode()).hexdigest()
            db.session.commit()
            return redirect(url_for('home'))
    return render_template('mdp-modif.html', form = f)

@app.route('/home', methods=['GET','POST'])
@login_required
@roles("Administrateur","Organisateur") #! A modifier pour les rôles
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

@app.route('/home/details-offre/<int:id_offre>', methods=['GET','POST'])
@login_required
def details_offre(id_offre):
    f = ReponseForm()
    o = Offre.query.get(id_offre)
    if not o:
        return redirect(url_for("home"))
    if f.validate_on_submit():
        r = Reponse()
        r.desc_rep = f.description.data
        r.budget = f.cotisation_apportee.data
        r.id_utilisateur = current_user.id_utilisateur
        r.id_offre = o.id_offre
        db.session.add(r)
        db.session.commit()
        return redirect(url_for('mes_offres'))
    return render_template('details_offre.html', offre=o, form = f)

@app.route('/home/repondre-offre/<int:id_offre>', methods=['GET','POST'])
@login_required
def repondre_offre(id_offre):
    f = ReponseForm()
    o = Offre.query.get(id_offre)
    if not o:
        return redirect(url_for("home"))
    if f.validate_on_submit():
        r = Reponse()
        r.desc_rep = f.description.data
        r.budget = f.cotisation_apportee.data
        r.id_utilisateur = current_user.id_utilisateur
        r.id_offre = o.id_offre
        db.session.add(r)
        db.session.commit()
        return redirect(url_for('mes_offres'))
    return render_template('repondre-offre.html', offre=o, form = f)

@app.route('/home/profil', methods=['GET','POST'])
def modifier_profil():
    """Renvoie la page de modification du profil

    Returns:
        profil.html: Une page de modification du profil
    """
    f = UpdateUser()
    if f.validate_on_submit():
        if f.validate():
            user = current_user  # Récupérer l'utilisateur actuel via Flask-Login
            user.prenom_utilisateur = f.prenom_user.data
            user.nom_utilisateur = f.nom_user.data
            user.email_utilisateur = f.email.data
            print(f.prenom_user.data)
            db.session.commit()
            #file = f.img.data
            #if file:
                #file.save(os.path.join("src/static/img/profil", file.filename))
            return redirect(url_for('home'))
    f.nom_user.data = current_user.nom_utilisateur
    f.prenom_user.data = current_user.prenom_utilisateur
    f.email.data = current_user.email_utilisateur 
    return render_template('profil.html', form=f)

@app.route('/home/mes-reseaux')
def mes_reseaux():
    """Renvoie la page des réseaux

    Returns:
        mes-reseaux.html: Une page des réseaux de l'utilisateur
    """
    f = SelectReseauForm()
    f.reseaux.choices = [(reseau.id_reseau, reseau.nom_reseau) for reseau in Reseau.query.all()]
    return render_template('mes-reseaux.html', form=f)

@app.route('/home/mes-reseaux-admin', methods=['GET', 'POST'])
def mes_reseaux_admin():
    """Renvoie la page des réseaux administrateur

    Returns:
        mes-reseaux-admin.html: Une page des réseaux pour un organisateur
    """
    les_reseaux = Reseau.query.all()
    f_select_reseau = SelectReseauForm()
    f_select_reseau.reseaux.choices = [(reseau.id_reseau, reseau.nom_reseau) for reseau in les_reseaux]

    if f_select_reseau.validate_on_submit():
        reseau_id = f_select_reseau.reseaux.data
        return redirect(url_for('mes_reseaux_admin', reseau_id=reseau_id))

    reseau_id = request.args.get('reseau_id', type=int)
    if reseau_id is not None:
        f_select_reseau.reseaux.default = reseau_id
        reseau_id = f_select_reseau.reseaux.default
    else:
        f_select_reseau.reseaux.default = les_reseaux[0].id_reseau if les_reseaux else None
        reseau_id = f_select_reseau.reseaux.default
    f_select_reseau.process()

    f_add_reseau = ReseauForm()
    if f_add_reseau.validate_on_submit():
        r = Reseau()
        r.nom_reseau = f_add_reseau.nom_reseau.data
        db.session.add(r)
        db.session.commit()
        return redirect(url_for('mes_reseaux_admin'))
    reseau = Reseau.query.get(reseau_id)
    return render_template('mes-reseaux-admin.html', reseaux=les_reseaux, add_form=f_add_reseau, select_form=f_select_reseau, membres=[[membre.orga for membre in reseau.les_utilisateurs]], reseau_id=reseau_id)

@app.route('/home/mes-reseaux-admin/suppression_utilisateur/<int:id_reseau>/<int:id_utilisateur>', methods=['GET', 'POST'])
def suppression_utilisateur_reseau(id_reseau, id_utilisateur):
    """Supprime un utilisateur d'un réseau
    Args:
        id_reseau (int): L'identifiant du réseau
        id_utilisateur (int): L'identifiant de l'utilisateur à supprimer
    Returns:
        mes-reseaux-admin.html: Une page des réseaux pour un organisateur
    """
    utilisateur_reseau = Utilisateur_Reseau.query.filter_by(id_reseau=id_reseau, id_utilisateur=id_utilisateur).first()
    if utilisateur_reseau:
        db.session.delete(utilisateur_reseau)
        db.session.commit()
    return redirect(url_for('mes_reseaux_admin', reseau_id=id_reseau))

@app.route('/home/mes-reseaux-admin/ajout_utilisateur/<int:id_reseau>', methods=['GET', 'POST'])
def ajout_utilisateur_reseau(id_reseau):
    """Ajoute un utilisateur à un réseau
    Args:
        id_reseau (int): L'identifiant du réseau
    Returns:
        mes-reseaux-admin.html: Une page des réseaux pour un organisateur
    """
    reseau = Reseau.query.get(id_reseau)
    if not reseau:
        return redirect(url_for('mes_reseaux_admin'))
    form = AddUtilisateurReseauForm()
    liste_utilisateurs = [utilisateur.id_utilisateur for utilisateur in reseau.les_utilisateurs]
    form.utilisateur.choices = [(utilisateur.id_utilisateur, utilisateur.nom_utilisateur) for utilisateur in Utilisateur.query.all() if utilisateur.id_utilisateur not in liste_utilisateurs]
    if form.validate_on_submit():
        utilisateur_id = form.utilisateur.data
        utilisateur_reseau = Utilisateur_Reseau(id_reseau=id_reseau, id_utilisateur=utilisateur_id)
        db.session.add(utilisateur_reseau)
        db.session.commit()
        return redirect(url_for('mes_reseaux_admin', reseau_id=id_reseau))
    return render_template('add-utilisateur-reseau.html', form=form, reseau=reseau)

@app.route('/home/creation-offre', methods=['GET','POST'])
@login_required
def creation_offre():
    """Renvoie la page de création d'une offre

    Returns:
        creation-offre.html: Une page de création d'une offre
    """
    f = OffreForm()
    f.genre.choices = [(genre.id_genre, genre.nom_genre) for genre in Genre.query.all()]
    f.reseau.choices = [(reseau.id_reseau, reseau.nom_reseau) for reseau in Reseau.query.all()]
    if f.validate_on_submit(): # and f.validate(): # ! A implémenter quand on affiche les erreurs dans le formulaire
        o = Offre()
        o.nom_offre = f.nom_offre.data
        o.description = f.description.data
        o.date_limite = f.date_limite.data
        o.budget = f.budget.data
        o.cotisation_min = f.cotisation_min.data
        o.capacite_max = f.capacite_max.data
        o.capacite_min = f.capacite_min.data
        o.img = f.img.data
        o.etat = f.etat.data
        o.nom_loc = f.nom_loc.data
        o.date_deb = f.date_deb.data
        o.date_fin = f.date_fin.data
        o.id_utilisateur = current_user.id_utilisateur
        db.session.add(o)
        db.session.commit()
        id_offre = Offre.query.filter_by(nom_offre = o.nom_offre, description = o.description).first().id_offre

        d = Document() # ! pour l'instant il n'y a qu'un document par offre. Si ça marche pas, remplacer f.documents.data par list(f.documents.data) ou [f.documents.data]
        d.nom_doc = f.documents.data
        d.id_offre = id_offre
        
        db.session.add(d)
        db.session.commit()
        
        # for genre in f.genre.data: # ! pour l'instant il n'y a qu'un genre par offre. Si ��a marche pas, remplacer f.genre.data par list(f.genre.data) ou [f.genre.data]
        g = Genre.query.get(f.genre.data)
        
        g_o = Genre_Offre()
        g_o.id_genre = g.id_genre
        g_o.id_offre = id_offre
        db.session.add(g_o)
        db.session.commit()
            
        # for res in f.reseau.data(): # ! pour l'instant il n'y a qu'un reseau par offre. Si ça marche pas, remplacer f.reseau.data par list(f.reseau.data) ou [f.reseau.data]
        r = Reseau.query.get(f.reseau.data)
        
        o_r = Offre_Reseau()
        o_r.id_reseau = r.id_reseau
        o_r.id_offre = id_offre
        db.session.add(o_r)
        db.session.commit()
        return redirect(url_for('mes_offres'))
    return render_template('creation-offre.html', form=f)

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
    les_reponses = Reponse.query.filter_by(id_utilisateur=current_user.id_utilisateur).all()
    return render_template('mes-reponses.html', reponses=les_reponses)

@app.route('/home/genre', methods=['GET','POST'])
def genre():
    """Renvoie la page de création d'un genre

    Returns:
        creation-genre.html: Une page de création d'un genre
    """
    f = GenreForm()
    les_genres = Genre.query.all()
    if f.validate_on_submit():
        if f.validate():
            g = Genre()
            g.nom_genre = f.nom_genre.data
            db.session.add(g)
            db.session.commit()
            return redirect(url_for('genre'))
    return render_template('genre.html', form=f, genres=les_genres)

@app.route('/home/suppression_genre/<int:id_genre>', methods=['POST'])
def suppression_genre(id_genre):
    """Supprime un genre

    Args:
        id_genre (int): L'identifiant du genre à supprimer

    Returns:
        genre.html: Une page de création d'un genre
    """
    g = Genre.query.get(id_genre)
    if g:
        db.session.delete(g)
        db.session.commit()
    return redirect(url_for('genre'))


@app.route('/home/boite-reception')
def boite_reception():
    """Renvoie la page de la boite de réception

    Returns:
        boite-reception.html: Une page de la boite de réception
    """
    return render_template('boite-reception.html')

