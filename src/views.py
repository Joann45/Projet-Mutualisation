from src.models import Notification, Notification_Utilisateur
from .app import db
from flask import render_template, redirect, url_for, request
from flask_security import login_required, current_user, roles_required,  logout_user, login_user
from src.forms.UtilisateurForm import InscriptionForm, ConnexionForm, UpdateUser, UpdatePassword
from flask import render_template, redirect, url_for, request, send_from_directory, Blueprint
from src.forms.UtilisateurForm import InscriptionForm, ConnexionForm
from src.forms.OffreForm import OffreForm, ReponseForm, CommentaireForm
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
from src.models.Commentaire import Commentaire
from src.forms.ReseauForm import ReseauForm, AddUtilisateurReseauForm
from datetime import datetime
from hashlib import sha256
from flask_security import Security, SQLAlchemySessionUserDatastore
from src.forms.ReseauForm import SelectReseauForm
from src.forms.RechercheOffreForm import SelectRechercheOffreForm, SelectDateProximité
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import os
from functools import wraps
from flask import abort
from src.extensions import db, login_manager
from flask_mail import Message, Mail
from .config import mail


# Définir un Blueprint pour les vues
views_bp = Blueprint('views', __name__)

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


@views_bp.route('/home', methods=['GET', 'POST'])
@views_bp.route('/', methods=['GET', 'POST'])
@login_required
@roles("Administrateur", "Organisateur")  # A modifier pour les rôles
def home():
    """Renvoie la page d'accueil"""
    les_reseaux = [Reseau.query.get(res.id_reseau) for res in Utilisateur_Reseau.query.filter_by(id_utilisateur=current_user.id_utilisateur)]
    les_offres = [] #! A modifier plus tard pour trier par les plus populaires
    for res in les_reseaux:
        les_offres+=[Offre.query.get(offre.id_offre) for offre in Offre_Reseau.query.filter_by(id_reseau=res.id_reseau)]
    return render_template('home.html', offres=les_offres[:3])


@views_bp.route('/home/profil', methods=['GET','POST'])
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
            file = f.img.data
            if file:
                file_path = os.path.join("src/static/img/profil", str(current_user.id_utilisateur))
                file.save(file_path)
            db.session.commit()
            return redirect(url_for('views.home'))
    f.nom_user.data = current_user.nom_utilisateur
    f.prenom_user.data = current_user.prenom_utilisateur
    f.email.data = current_user.email_utilisateur 
    return render_template('profil.html', form=f)


@views_bp.route('/static/Documents/<int:id_d>-<int:id_o>', methods=['GET', 'POST'])
def get_documents(id_d, id_o):

    documents_folder = os.path.join("static", "Documents")
    file_name = Document.query.filter_by(id_doc=id_d).first()
    new_filename = f"{file_name.nom_doc}"
    return send_from_directory(
        documents_folder,
        str(id_d)+"-"+str(id_o),
        as_attachment=True,
        download_name=new_filename
    )


@views_bp.route('/home/rechercher/les-offres', methods=['GET', 'POST'])
@login_required
def rechercher():
    """_summary_

    Returns:
        _type_: _description_
    """

@views_bp.route('/home/creation-offre', defaults={'id_offre': None}, methods=['GET','POST'])    
@views_bp.route('/home/creation-offre/<int:id_offre>', methods=['GET','POST'])
@login_required
def creation_offre(id_offre=None):
    """Renvoie la page de création d'une offre

    Returns:
        creation-offre.html: Une page de création d'une offre
    """

    o = Offre.query.get(id_offre) if id_offre else None
    print(o,"oooooo")

    f = OffreForm()
    f.genre.choices = [(genre.id_genre, genre.nom_genre) for genre in Genre.query.all()]

    les_reseaux = [Reseau.query.get(res.id_reseau) for res in Utilisateur_Reseau.query.filter_by(id_utilisateur = current_user.id_utilisateur)]
    f_select_reseau = SelectRechercheOffreForm()
    f_select_reseau.reseaux.choices = [(reseau.id_reseau, reseau.nom_reseau) for reseau in les_reseaux]

    id_reseaux_elu =  f_select_reseau.reseaux.data
    les_reseaux_elu = []
    
    if f.validate_on_submit(): # and f.validate(): # ! A implémenter quand on affiche les erreurs dans le formulaire
        if o is None:
            o = Offre()
            o.nom_offre = f.nom_offre.data
            o.description = f.description.data
            o.date_limite = f.date_limite.data
            o.budget = f.budget.data
            o.cotisation_min = f.cotisation_min.data
            o.capacite_max = f.capacite_max.data
            o.capacite_min = f.capacite_min.data
            #o.img = f.img.data
            o.etat = "brouillon"
            o.nom_loc = f.nom_loc.data
            o.date_deb = f.date_deb.data
            o.date_fin = f.date_fin.data
            o.id_utilisateur = current_user.id_utilisateur
            file_o = f.img.data
            db.session.add(o)
            db.session.commit()
            id_offre = o.id_offre
            if not file_o:
                o.img = "0"
            else:
                file_path = os.path.join("src/static/img/offre", str(id_offre))
                file_o.save(file_path)
                o.img = id_offre
            db.session.commit()
            file = f.documents.data
            if file:
                d = Document() # ! pour l'instant il n'y a qu'un document par offre. Si ça marche pas, remplacer f.documents.data par list(f.documents.data) ou [f.documents.data]
                filename = secure_filename(file.filename)
                d.nom_doc = filename
                d.id_offre = id_offre
                db.session.add(d)
                db.session.commit()
                file_path = os.path.join("src/static/Documents", str(d.id_doc)+"-"+str(id_offre)) 
                file.save(file_path)
                o.docs = True
            else:
                o.docs = False
            # for genre in f.genre.data: # ! pour l'instant il n'y a qu'un genre par offre. Si ��a marche pas, remplacer f.genre.data par list(f.genre.data) ou [f.genre.data]
            g = Genre.query.get(f.genre.data)
            g_o = Genre_Offre()
            g_o.id_genre = g.id_genre
            g_o.id_offre = id_offre
            db.session.add(g_o)
            db.session.commit()

            for r in id_reseaux_elu:
                les_reseaux_elu.append(f_select_reseau.reseaux.choices[int(r)-1][0])

            for r in les_reseaux_elu:
                o_r = Offre_Reseau()
                o_r.id_reseau = r
                o_r.id_offre = id_offre
                db.session.add(o_r)
                db.session.commit()
            return redirect(url_for('mes_offres'))
        else:
            o.nom_offre = f.nom_offre.data
            o.description = f.description.data
            o.date_limite = f.date_limite.data
            o.budget = f.budget.data
            o.cotisation_min = f.cotisation_min.data
            o.capacite_max = f.capacite_max.data
            o.capacite_min = f.capacite_min.data
            #o.img = f.img.data
            o.etat = "brouillon"
            o.nom_loc = f.nom_loc.data
            o.date_deb = f.date_deb.data
            o.date_fin = f.date_fin.data
            o.id_utilisateur = current_user.id_utilisateur
            file_o = f.img.data
            db.session.commit()
            if not file_o:
                o.img = "0"
            else:
                file_path = os.path.join("src/static/img/offre", str(id_offre))
                file_o.save(file_path)
                o.img = id_offre
            db.session.commit()
            file = f.documents.data
            if file:
                d = Document()
                filename = secure_filename(file.filename)
                d.nom_doc = filename
                d.id_offre = id_offre
                db.session.commit()
                file_path = os.path.join("src/static/Documents", str(d.id_doc)+"-"+str(id_offre)) 
                file.save(file_path)
                o.docs = True
            else:
                o.docs = False
            # for genre in f.genre.data: # ! pour l'instant il n'y a qu'un genre par offre. Si ��a marche pas, remplacer f.genre.data par list(f.genre.data) ou [f.genre.data]
            g = Genre.query.get(o.les_genres[0].id_genre)
            # g_o = Genre_Offre()
            g_o = Genre_Offre.query.filter_by(id_offre=id_offre).first()
            g_o.id_genre = g.id_genre
            g_o.id_offre = id_offre
            db.session.commit()

            for r in id_reseaux_elu:
                les_reseaux_elu.append(f_select_reseau.reseaux.choices[int(r)-1][0])

            for r in les_reseaux_elu:
                o_r = Offre_Reseau()
                o_r.id_reseau = r
                o_r.id_offre = id_offre
                db.session.commit()
            print("azeazeaze")
            return redirect(url_for('mes_offres'))
    if o:
        f.nom_offre.data = o.nom_offre
        f.description.data = o.description
        f.date_limite.data = o.date_limite
        f.budget.data = o.budget
        f.cotisation_min.data = o.cotisation_min
        f.capacite_max.data = o.capacite_max
        f.capacite_min.data = o.capacite_min
        f.nom_loc.data = o.nom_loc
        f.date_deb.data = o.date_deb
        f.date_fin.data = o.date_fin
        f.genre.data = o.les_genres[0].id_genre
        f.img.data = o.img
        # f.documents.data = o.les_documents[0].id_doc
    
    return render_template('creation-offre.html',reseaux=les_reseaux, form=f, form_reseaux=f_select_reseau, offre=o)

@views_bp.route('/home/visualiser-reponses-offres') #! A MODIFIER QUAND LA PAGE DE L'OFFRE SERA CREEE
def visualiser_offre():
    """Renvoie la page de visualisation des réponses aux offres

    Returns:
        visualiser-reponses-offres.html: Une page de visualisation des réponses aux offres
    """
    
    return render_template('visualiser-reponses-offres.html')

@views_bp.route('/home/mes-offres/publication/<int:id_offre>', methods=['GET','POST'])
@login_required
def definir_etat(id_offre):
    """
    Définit l'état d'un objet Offre à l'état spécifié.
    Args:
        id_offre (int): L'identifiant de l'offre à mettre à jour.
    Returns:
        None
    """

    o = Offre.query.get(id_offre)
    print(o)
    if o :
        if o.etat == "publiée" : 
            o.etat = "brouillon"
        else : 
            o.etat = "publiée"
        db.session.commit()
    return redirect(url_for('offre.mes_offres'))

@views_bp.route('/home/genre', methods=['GET','POST'])
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
            return redirect(url_for('creation_offre'))
    return render_template('genre.html', form=f, genres=les_genres)

@views_bp.route('/home/suppression_genre/<int:id_genre>', methods=['POST'])
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

    return redirect(url_for('views.genre'))

@views_bp.route('/home/boite-reception')
def boite_reception():
    """Renvoie la page de la boite de réception"""
    les_notifs_utilisateurs = Notification_Utilisateur.query.filter_by(id_utilisateur=current_user.id_utilisateur).all()
    les_notifs = Notification.query.filter(Notification.id_notif.in_([notif.id_notif for notif in les_notifs_utilisateurs])).all()
    return render_template('boite-reception.html', les_notifs = les_notifs)
