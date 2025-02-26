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
from src.forms.RechercheOffreForm import SelectRechercheOffreForm, SelectDateProximité
from werkzeug.utils import secure_filename
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import os
from functools import wraps
from flask import abort

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
        Reponse.query.filter_by(id_offre=id_offre).delete()
        Offre_Reseau.query.filter_by(id_offre=id_offre).delete()
        Genre_Offre.query.filter_by(id_offre=id_offre).delete()
        db.session.delete(o)
        db.session.commit()
    return redirect(url_for('offre.mes_offres'))


@offre_bp.route('/home/creation-offre', methods=['GET','POST'])
@login_required
def creation_offre():
    """Renvoie la page de création d'une offre

    Returns:
        creation-offre.html: Une page de création d'une offre
    """
    f = OffreForm()
    f.genre.choices = [(genre.id_genre, genre.nom_genre) for genre in Genre.query.all()]

    les_reseaux = [Reseau.query.get(res.id_reseau) for res in Utilisateur_Reseau.query.filter_by(id_utilisateur = current_user.id_utilisateur)]
    f_select_reseau = SelectRechercheOffreForm()
    f_select_reseau.reseaux.choices = [(reseau.id_reseau, reseau.nom_reseau) for reseau in les_reseaux]

    id_reseaux_elu =  f_select_reseau.reseaux.data
    les_reseaux_elu = []
    if f.validate_on_submit(): # and f.validate(): # ! A implémenter quand on affiche les erreurs dans le formulaire
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
            if not os.path.exists("src/static/Documents"):
                os.makedirs("src/static/Documents")
            file_path = os.path.join("src/static/Documents", str(d.id_doc)+"-"+str(id_offre))
            file.save(file_path)
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
        return redirect(url_for('offre.mes_offres'))
    return render_template('creation-offre.html',reseaux=les_reseaux, form=f, form_reseaux=f_select_reseau)

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

    proximité_date = SelectDateProximité()
    proximité_date.proxi.choices = ["Plus Proche", "Moins Proche"] #afficage  de filtre de date d'expiration

    if proximité_date.proxi.data == None : #Si pas de choix la choix de base est plus proche pour la date d'expiration
        proximité_date.proxi.default = "Plus Proche"
        proximité_date.process()

    id_reseaux_elu =  f_select_reseau.reseaux.data #recupere l'information des reseaux choisi 
    les_reseaux_elu = []


    proxi_elu = proximité_date.proxi.data #recupere l'information de date d'expiration

   
    if proximité_date.validate_on_submit() or f_select_reseau.validate_on_submit(): #Si Choix fait 
        

        for id_r in id_reseaux_elu:
            les_reseaux_elu.append(Reseau.query.get(id_r))
    

    if les_reseaux_elu != []: #Si des reseux était choixi par utilisateur
        offre_reseau = [Offre_Reseau.query.filter_by(id_reseau=reseau.id_reseau).all() for reseau in les_reseaux_elu]
       
        

    else: #Si aucun choit était fait 
        
        offre_reseau = [Offre_Reseau.query.filter_by(id_reseau=reseau.id_reseau).all() for reseau in Utilisateur_Reseau.query.filter_by(id_utilisateur=current_user.id_utilisateur).all()]
        
    offres = [Offre.query.filter_by(id_offre=o.id_offre, id_utilisateur=current_user.id_utilisateur).all() for o in offre_reseau[0]]
    les_offres = []
    for offre in offres:
        les_offres+=offre

    if proxi_elu == "Plus Proche":
        les_offres.sort(key=lambda o:o.date_limite)
    else: 
        les_offres.sort(reverse=True,key=lambda o:o.date_limite)

    return render_template('mes-offres.html', offres=les_offres,form=f_select_reseau,formd=proximité_date)



def get_reseaux_for_user(user):
    """Récupère les réseaux en fonction du rôle de l'utilisateur."""
    if user.is_admin():
        return Reseau.query.all()
    return Reseau.query.filter(Reseau.les_utilisateurs.any(id_utilisateur=user.id_utilisateur)).all()

@offre_bp.route('/home/les-offres', methods=["POST","GET"])
def les_offres():
    """Renvoie la page des offres

    Returns:
        les-offres.html: Une page des offres
    """
    les_reseaux = get_reseaux_for_user(current_user)
    f_select_reseau = SelectRechercheOffreForm()
    f_select_reseau.reseaux.choices = [(reseau.id_reseau, reseau.nom_reseau) for reseau in les_reseaux]

    proximité_date = SelectDateProximité()
    proximité_date.proxi.choices = ["Plus Proche", "Moins Proche"]

    if proximité_date.proxi.data == None :
        proximité_date.proxi.default = "Plus Proche"
        proximité_date.process()
    
    proxi_elu = proximité_date.proxi.data

    id_reseaux_elu =  f_select_reseau.reseaux.data
    les_reseaux_elu = []
    
    
        
    if proximité_date.validate_on_submit() or f_select_reseau.validate_on_submit():
        for id_r in id_reseaux_elu:
            print(Reseau.query.get(id_r))
            les_reseaux_elu.append(Reseau.query.get(id_r))
    


    if les_reseaux_elu != []:
        offre_reseau = [Offre_Reseau.query.filter_by(id_reseau=reseau.id_reseau,).all() for reseau in les_reseaux_elu]
        
    else: 
        
        offre_reseau = [Offre_Reseau.query.filter_by(id_reseau=reseau.id_reseau).all() for reseau in Utilisateur_Reseau.query.filter_by(id_utilisateur=current_user.id_utilisateur).all()]
             
               
    if len(offre_reseau) != 0: 
        offres = [Offre.query.filter_by(id_offre=o.id_offre, etat="publiée").all() for o in offre_reseau[0]]
    les_offres = []
    for offre in offres:
        les_offres+=offre

    if proxi_elu == "Plus Proche":
        les_offres.sort(key=lambda o:o.date_limite)
    else: 
        les_offres.sort(reverse=True,key=lambda o:o.date_limite)


    return render_template('les-offres.html', offres=les_offres,form=f_select_reseau,formd=proximité_date)
