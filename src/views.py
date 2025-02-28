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
from src.models.Favoris import Favoris
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
    #les_reseaux = [Reseau.query.get(res.id_reseau) for res in Utilisateur_Reseau.query.filter_by(id_utilisateur=current_user.id_utilisateur)]
    # les_offres = Offre.query.filter(Offre.etat == "publiée",Offre.id_offre.in_([o_r.offre.id_offre for o_r in offre_reseau[0]]), Offre.date_limite > dt.date.today())
    #for res in les_reseaux:
    #    les_offres+=[Offre.query.get(offre.id_offre) for offre in Offre_Reseau.query.filter_by(id_reseau=res.id_reseau)]
    offres = Offre.query.filter(Offre.etat == "publiée", Offre.date_limite > datetime.now()).all()
    les_reseaux = current_user.les_reseaux
    les_offres = []
    for offre in offres:
        if len(set(offre.les_reseaux).intersection(les_reseaux)) > 0:
            les_offres.append(offre)
    return render_template('home.html', offres=les_offres[:3])


@views_bp.route('/home/profil', methods=['GET','POST'])
@login_required
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
            user.img_utilisateur = "0"
            file = f.img.data
            if file:
                user.img_utilisateur = user.id_utilisateur
                file_path = os.path.join("src/static/img/profil", str(current_user.id_utilisateur))
                file.save(file_path)
            db.session.commit()
            return redirect(url_for('views.home'))
    f.nom_user.data = current_user.nom_utilisateur
    f.prenom_user.data = current_user.prenom_utilisateur
    f.email.data = current_user.email_utilisateur 
    return render_template('profil.html', form=f)


@views_bp.route('/static/Documents/<int:id_d>-<int:id_o>', methods=['GET', 'POST'])
@login_required
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

@views_bp.route('/home/visualiser-reponses-offres') #! A MODIFIER QUAND LA PAGE DE L'OFFRE SERA CREEE
@login_required
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
    if o :
        if o.etat == "publiée" : 
            o.etat = "brouillon"
        else : 
            o.etat = "publiée"
        db.session.commit()
    return redirect(url_for('offre.details_offre',id_offre=id_offre))

@views_bp.route('/home/genre', methods=['GET','POST'])
@login_required
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
@login_required
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
@login_required
def boite_reception():
    """Renvoie la page de la boite de réception"""
    les_notifs_utilisateurs = Notification_Utilisateur.query.filter_by(id_utilisateur=current_user.id_utilisateur).all()
    les_notifs = Notification.query.filter(Notification.id_notif.in_([notif.id_notif for notif in les_notifs_utilisateurs])).all()
    return render_template('boite-reception.html', les_notifs = les_notifs,aucune_notifs = len(les_notifs)==0)

@views_bp.route('/home/visualiser_profil/<int:id_utilisateur>', methods=['POST','GET'])
@login_required
def visualiser_profil(id_utilisateur):
    return render_template('visualiser_profil.html', utilisateur=Utilisateur.query.get(id_utilisateur))

@views_bp.route('/home/mes-favoris', methods=['POST','GET'])
@views_bp.route('/home/mes-favoris/<int:page>', methods=['POST','GET'])
@login_required
def mes_favoris(page=1):
    
    les_favoris = Favoris.query.filter_by(id_utilisateur=current_user.id_utilisateur).all()
    les_offres = Offre.query.filter(Offre.id_offre.in_([offre.id_offre for offre in les_favoris]))
    les_offres = db.paginate(les_offres, page=page, per_page=5)
    
    return render_template('mes-favoris.html', les_offres = les_offres,aucune_offre = len(les_offres.items)==0)