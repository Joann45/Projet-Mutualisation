from src.app import db
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
from src.forms.RechercheOffreForm import SelectRechercheOffreForm, SelectStatueOffre, SelectDateProximité
from werkzeug.utils import secure_filename
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import os
from functools import wraps
from flask import abort
import datetime as dt

offre_bp = Blueprint('offre', __name__, template_folder='templates')
print(os.getcwd())

@offre_bp.route('/home/details-offre/<int:id_offre>', methods=['GET','POST'])
@login_required
def details_offre(id_offre):
    o = Offre.query.get(id_offre)
    commentaireForm = CommentaireForm()
    if commentaireForm.validate_on_submit():
        c = Commentaire()
        c.texte_commentaire = commentaireForm.texte_commentaire.data
        c.id_offre = id_offre
        c.id_utilisateur = current_user.id_utilisateur
        c.date_commentaire = datetime.now()
        db.session.add(c)
        db.session.commit()
        return redirect(url_for('offre.details_offre', id_offre=id_offre))
    verif = 1
    if not o:
        return redirect(url_for("home"))
    if Reponse.query.filter_by(id_utilisateur=current_user.id_utilisateur, id_offre=id_offre).first():
        
        verif = 2
    elif o.utilisateur == current_user or current_user.role_id == 2:
        verif = 3
    return render_template('details-offre.html', offre=o, verif=verif, commentaireForm=commentaireForm)


@offre_bp.route('/home/mes-offres/suppression-offre/<int:id_offre>', methods=['GET', 'POST'])
def suppression_offre(id_offre):
    """Supprime une offre

    Args:
        id_offre (int): L'identifiant de l'offre à supprimer

    Returns:
        mes-offres.html: Une page des offres de l'utilisateur
    """
    o = Offre.query.get(id_offre)
    if o:
        if o.etat == "brouillon":
            Reponse.query.filter_by(id_offre=id_offre).delete()
            Commentaire.query.filter_by(id_offre=id_offre).delete()
            Document.query.filter_by(id_offre=id_offre).delete()
            Offre_Reseau.query.filter_by(id_offre=id_offre).delete()
            Genre_Offre.query.filter_by(id_offre=id_offre).delete()
            db.session.delete(o)
            db.session.commit()
    return redirect(url_for('offre.mes_offres'))


def create_new_offer(form):
    """Crée une nouvelle offre à partir du formulaire."""
    o = Offre()
    o.nom_offre = form.nom_offre.data
    o.description = form.description.data
    o.date_limite = form.date_limite.data
    o.budget = form.budget.data
    o.cotisation_min = form.cotisation_min.data
    o.capacite_max = form.capacite_max.data
    o.capacite_min = form.cotisation_min.data
    o.etat = "brouillon"
    o.nom_loc = form.nom_loc.data
    o.date_deb = form.date_deb.data
    o.date_fin = form.date_fin.data
    o.id_utilisateur = current_user.id_utilisateur
    db.session.add(o)
    db.session.commit()  # Pour obtenir l'id_offre généré
    return o

def update_offer(o, form):
    """Met à jour l'offre existante avec les valeurs du formulaire."""
    o.nom_offre = form.nom_offre.data
    o.description = form.description.data
    o.date_limite = form.date_limite.data
    o.budget = form.budget.data
    o.cotisation_min = form.cotisation_min.data
    o.capacite_max = form.capacite_max.data
    o.capacite_min = form.cotisation_min.data
    o.etat = "brouillon"
    o.nom_loc = form.nom_loc.data
    o.date_deb = form.date_deb.data
    o.date_fin = form.date_fin.data
    o.id_utilisateur = current_user.id_utilisateur
    db.session.commit()
    return o

def process_offer_image(o, form):
    """Traite l'image de l'offre (sauvegarde ou valeur par défaut)."""
    file_o = form.img.data
    if not file_o:
        o.img = "0"
    else:
        file_path = os.path.join("src/static/img/offre", str(o.id_offre))
        file_o.save(file_path)
        o.img = o.id_offre
    db.session.commit()

def process_offer_document(o, form):
    """Traite le(s) document(s) attaché(s) à l'offre."""
    file = form.documents.data
    if file:
        # Ici on considère qu'il y a éventuellement plusieurs documents
        for doc in file:
            d = Document()
            filename = secure_filename(doc.filename)
            d.nom_doc = filename
            d.id_offre = o.id_offre
            db.session.add(d)
            db.session.commit()
            file_path = os.path.join("src/static/Documents", f"{d.id_doc}-{o.id_offre}")
            doc.save(file_path)
            o.docs = True
    else:
        o.docs = False
    db.session.commit()

def process_offer_genre(o, form):
    """Associe l'offre au genre sélectionné."""
    g = Genre.query.get(form.genre.data)
    # Pour la création, on ajoute un nouveau lien, sinon on met à jour le lien existant
    g_o = Genre_Offre.query.filter_by(id_offre=o.id_offre).first()
    if not g_o:
        g_o = Genre_Offre()
        g_o.id_offre = o.id_offre
        db.session.add(g_o)
    g_o.id_genre = g.id_genre
    db.session.commit()

def process_offer_reseaux(o, form_reseaux):
    """Réassocie les réseaux sélectionnés à l'offre."""
    # Suppression des anciennes associations
    Offre_Reseau.query.filter_by(id_offre=o.id_offre).delete()
    db.session.commit()
    for r in form_reseaux.reseaux.data:
        o_r = Offre_Reseau()
        o_r.id_reseau = r
        o_r.id_offre = o.id_offre
        db.session.add(o_r)
        db.session.commit()

def populate_offer_form(o, form, form_reseaux):
    """Préremplit les formulaires avec les valeurs de l'offre existante."""
    form.nom_offre.data = o.nom_offre
    form.description.data = o.description
    form.date_limite.data = o.date_limite
    form.budget.data = o.budget
    form.cotisation_min.data = o.cotisation_min
    form.capacite_max.data = o.capacite_max
    form.capacite_min.data = o.capacite_min
    form.nom_loc.data = o.nom_loc
    form.date_deb.data = o.date_deb
    form.date_fin.data = o.date_fin
    if o.les_genres:
        form.genre.data = o.les_genres[0].id_genre
    # Récupération des réseaux déjà associés
    reseaux_selected = Offre_Reseau.query.filter_by(id_offre=o.id_offre).all()
    form_reseaux.reseaux.default = [r.id_reseau for r in reseaux_selected]
    form_reseaux.process()
    form.img.data = o.img

@offre_bp.route('/home/creation-offre', defaults={'id_offre': None}, methods=['GET','POST'])
@offre_bp.route('/home/creation-offre/<int:id_offre>', methods=['GET','POST'])
@login_required
def creation_offre(id_offre=None):
    """Renvoie la page de création d'une offre.
       Si id_offre est fourni, l'offre est modifiée.
    """
    o = Offre.query.get(id_offre) if id_offre else None

    f = OffreForm()
    f.genre.choices = [(genre.id_genre, genre.nom_genre) for genre in Genre.query.all()]

    les_reseaux = [Reseau.query.get(res.id_reseau)
                   for res in Utilisateur_Reseau.query.filter_by(id_utilisateur=current_user.id_utilisateur)]
    f_select_reseau = SelectRechercheOffreForm()
    f_select_reseau.reseaux.choices = [(reseau.id_reseau, reseau.nom_reseau) for reseau in les_reseaux]

    if f.validate_on_submit():
        # Création ou mise à jour de l'offre
        if o is None:
            o = create_new_offer(f)
        else:
            o = update_offer(o, f)

        process_offer_image(o, f)
        process_offer_document(o, f)
        process_offer_genre(o, f)
        process_offer_reseaux(o, f_select_reseau)
        return redirect(url_for('offre.mes_offres'))

    if o:
        populate_offer_form(o, f, f_select_reseau)

    return render_template('creation-offre.html',
                           reseaux=les_reseaux,
                           form=f,
                           form_reseaux=f_select_reseau,
                           offre=o)

@offre_bp.route('/home/visualiser-reponses-offres') #! A MODIFIER QUAND LA PAGE DE L'OFFRE SERA CREEE
def visualiser_offre():
    """Renvoie la page de visualisation des réponses aux offres

    Returns:
        visualiser-reponses-offres.html: Une page de visualisation des réponses aux offres
    """
    
    return render_template('visualiser-reponses-offres.html')





@offre_bp.route('/home/mes-offres', methods=["POST","GET"])
@login_required
def mes_offres():
    """Renvoie la page des offres de l'utilisateur

    Returns:
        mes-offres.html: Une page des offres de l'utilisateur
    """
    

    les_reseaux = get_reseaux_for_user(current_user) #les reseaux de l'utilisateur currrent 
    f_select_reseau = SelectRechercheOffreForm()
    f_select_reseau.reseaux.choices = [(reseau.id_reseau, reseau.nom_reseau) for reseau in les_reseaux] #affichage  des reseaux de l'utilisateur currrent 

    proximite_date = SelectDateProximité()
    proximite_date.proxi.choices = ["Plus Proche", "Moins Proche"] #afficage  de filtre de date d'expiration

    statue_offre = SelectStatueOffre()
    statue_offre.statue.choices = ["Tous","À venir","En cours","Expiré"] #affichage de filtre des status 

    if proximite_date.proxi.data == None : #Si pas de choix la choix de base est plus proche pour la date d'expiration
        proximite_date.proxi.default = "Plus Proche"
        proximite_date.process()

    if statue_offre.statue.data == None : #Si pas de choix insi que choix par default est à venir
        statue_offre.statue.default = "Tous"
        statue_offre.process()

  
    les_reseaux_elu = []


    proxi_elu = proximite_date.proxi.data #recupere l'information de date d'expiration

    statue_elu = statue_offre.statue.data #recupere l'infomration de statue choisi

   
    if proximite_date.validate_on_submit() or f_select_reseau.validate_on_submit(): #Si Choix fait 
        

        for id_r in f_select_reseau.reseaux.data: #recupere l'information des reseaux choisi
            les_reseaux_elu+=Reseau.query.filter_by(id_reseau=id_r).all()
        
    

    if les_reseaux_elu != []: #Si des reseux était choixi par utilisateur
        offre_reseau = [Offre_Reseau.query.filter_by(id_reseau=reseau.id_reseau).all() for reseau in les_reseaux_elu]
        
       
        

    else: #Si aucun choit était fait 
        
        offre_reseau = [Offre.query.filter_by(id_utilisateur=current_user.id_utilisateur).all()]
    
    print(les_reseaux_elu)
    offres = []
    for ofr in offre_reseau:   

        liste = [Offre.query.filter_by(id_offre=o.id_offre, id_utilisateur=current_user.id_utilisateur).all() for o in ofr]
        for ele in liste:
            offres += ele
        print(offres)
        
    
    offres= set(offres)
    offres = list(offres)
    les_offres = []       

    current_date = dt.date.today()

    for offre in offres:
        if statue_elu == statue_offre.statue.choices[0] or len(offre)==0:
            les_offres.append(offre)
        elif statue_elu == statue_offre.statue.choices[1]:#cas de à venir d'etre choisi
             
            if offre.date_limite>=current_date: #date de limite apres la date currant
                les_offres.append(offre)

        elif statue_elu == statue_offre.statue.choices[2]:#cas de en cours 
            
            if offre.date_deb <= current_date <= offre.date_fin: #date de debut déja passé et  l'offre n'est pas encore dini  
                les_offres.append(offre)

        elif statue_elu == statue_offre.statue.choices[3]: #case de expiré 
            
            if offre.date_fin<current_date:
                les_offres.append(offre)
        

    if proxi_elu == "Plus Proche": #cas de plus proche d'etre choisi
        les_offres.sort(key=lambda o:o.date_limite)
    else: #cas de moins proche d'etre choisi
        les_offres.sort(reverse=True,key=lambda o:o.date_limite)


    return render_template('mes-offres.html', offres=les_offres,form=f_select_reseau,formd=proximite_date,formstatue=statue_offre)


def get_reseaux_for_user(user):
    """Récupère les réseaux en fonction du rôle de l'utilisateur."""
    if user.is_admin():
        return Reseau.query.all()
    return Reseau.query.filter(Reseau.les_utilisateurs.any(id_utilisateur=user.id_utilisateur)).all()

@offre_bp.route('/home/les-offres', methods=["POST","GET"])
@offre_bp.route('/home/les-offres/<int:page>', methods=["POST","GET"])
@login_required
def les_offres(page=1):
    """Renvoie la page des offres
    Returns:
        les-offres.html: Une page des offres
    """
    les_reseaux = get_reseaux_for_user(current_user)
    f_select_reseau = SelectRechercheOffreForm()
    f_select_reseau.reseaux.choices = [(reseau.id_reseau, reseau.nom_reseau) for reseau in les_reseaux]
    proximite_date = SelectDateProximité()
    proximite_date.proxi.choices = ["Plus Proche", "Moins Proche"]
    if proximite_date.proxi.data == None :
        proximite_date.proxi.default = "Plus Proche"
        proximite_date.process()

    proxi_elu = proximite_date.proxi.data

    id_reseaux_elu =  f_select_reseau.reseaux.data
    les_reseaux_elu = []

    if proximite_date.validate_on_submit() or f_select_reseau.validate_on_submit():
        for id_r in id_reseaux_elu:
            print(Reseau.query.get(id_r))
            les_reseaux_elu.append(Reseau.query.get(id_r))
    if les_reseaux_elu != []:
        offre_reseau = [Offre_Reseau.query.filter_by(id_reseau=reseau.id_reseau,).all() for reseau in les_reseaux_elu]
    else: 
        
        offre_reseau = [Offre_Reseau.query.filter_by(id_reseau=reseau.id_reseau).all() for reseau in Utilisateur_Reseau.query.filter_by(id_utilisateur=current_user.id_utilisateur).all()]
             
               
    if len(offre_reseau) != 0: 
        les_offres = Offre.query.filter(Offre.etat == "publiée",Offre.id_offre.in_([o_r.offre.id_offre for o_r in offre_reseau[0]]), Offre.date_limite > dt.date.today())
    else:
        les_offres = []
    if proxi_elu == "Plus Proche":
        les_offres.order_by(Offre.date_limite)
    else: 
        les_offres.order_by(Offre.date_limite.desc())
    les_offres = db.paginate(les_offres, per_page=5, page=page)
    return render_template('les-offres.html', offres=les_offres,form=f_select_reseau,formd=proximite_date)

@offre_bp.route('/home/details-offre/suppression-commentaire/<int:id_commentaire>', methods=['GET', 'POST'])
@login_required
def suppression_commentaire(id_commentaire):
    commentaire = Commentaire.query.get(id_commentaire)
    if not commentaire:
        abort(404)
    # Vérifier que le commentaire appartient à l'utilisateur
    if commentaire.id_utilisateur != current_user.id_utilisateur:
        abort(403)
    id_offre = commentaire.id_offre
    db.session.delete(commentaire)
    db.session.commit()
    return redirect(url_for('offre.details_offre', id_offre=id_offre))
