from src.extensions import db
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

reponse_bp = Blueprint('reponses', __name__, template_folder='templates')

@reponse_bp.route('/home/visualiser-reponses-offre/<int:id_offre>') #! A MODIFIER QUAND LA PAGE DE L'OFFRE SERA CREEE
@login_required
def visualiser_reponses_offre(id_offre):
    """Renvoie la page de visualisation des réponses aux offres

    Returns:
        visualiser-reponses-offre.html: Une page de visualisation des réponses aux offres
    """
    verif = True
    les_reponses = Reponse.query.filter_by(id_offre=id_offre)
    if not les_reponses:
        return render_template('visualiser-reponses-offre.html', None)
    o = Offre.query.get(id_offre)
    if not o.img:
        verif = False
    return render_template('visualiser-reponses-offre.html',verif=verif, offre=o, reponses=les_reponses)  



@login_required
def get_reseaux_for_user(user):
    """Récupère les réseaux en fonction du rôle de l'utilisateur."""
    if user.is_admin():
        return Reseau.query.all()
    return Reseau.query.filter(Reseau.les_utilisateurs.any(id_utilisateur=user.id_utilisateur)).all()

@reponse_bp.route('/home/mes-offres/mes-reponses/suppression-reponse/<int:id_utilisateur>/<int:id_offre>', methods=['GET', 'POST'])
@login_required
def suppression_reponse(id_utilisateur, id_offre):
    """Supprime une réponse a une offre

    Args:
        id_reponse (int): L'identifiant de la réponse à supprimer

    Returns:
        mes-reponses.html: Une page des réponses de l'utilisateur
    """
    r = Reponse.query.filter_by(id_utilisateur=id_utilisateur,id_offre=id_offre).first()
    if r:
        Reponse.query.filter_by(id_utilisateur=id_utilisateur,id_offre=id_offre).delete()
        db.session.delete(r)
        db.session.commit()
    return redirect(url_for('reponses.mes_reponses'))

@reponse_bp.route('/home/mes-offres/mes-reponses', methods=["POST","GET"])
@login_required
def mes_reponses():
    """Renvoie la page des réponses de l'utilisateur

    Returns:
        mes-reponses.html: Une page des réponses de l'utilisateur
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
            les_reseaux_elu.append(Reseau.query.get(id_r))
    


    if les_reseaux_elu != []:
        offre_reseau = [Offre_Reseau.query.filter_by(id_reseau=reseau.id_reseau).all() for reseau in les_reseaux_elu]
        offres = [Offre.query.get(o.id_offre) for o in offre_reseau[0]]
        les_reponses = []
        
        
        if proxi_elu == "Plus Proche":
            les_rep = [Reponse.query.filter_by(id_offre=offre.id_offre, id_utilisateur=current_user.id_utilisateur).order_by(Reponse.date_fin).all() for offre in offres]
            for offre in les_rep:
                les_reponses += offre 
                
        else:
            les_rep = [Reponse.query.filter_by(id_offre=offre.id_offre, id_utilisateur=current_user.id_utilisateur).order_by(Reponse.date_fin.desc()).all() for offre in offres]
            for offre in les_rep:
                les_reponses += offre 
                

        
        

    else: 
        if proxi_elu == "Plus Proche":
            les_reponses = Reponse.query.filter_by(id_utilisateur=current_user.id_utilisateur).order_by(Reponse.date_fin.desc()).all()
        else: 
            les_reponses = Reponse.query.filter_by(id_utilisateur=current_user.id_utilisateur).order_by(Reponse.date_fin).all()

    return render_template('mes-reponses.html', reponses=les_reponses, form=f_select_reseau, formd=proximité_date)

    


@reponse_bp.route('/home/repondre-offre/<int:id_offre>', methods=['GET','POST'])
@login_required
def repondre_offre(id_offre):
    o = Offre.query.get(id_offre)
    f = ReponseForm(o)
    if not o:
        return redirect(url_for("home"))
    reponse = Reponse.query.filter_by(id_utilisateur=current_user.id_utilisateur, id_offre=id_offre).first()
    cot_tot = 0
    all_cot = Reponse.query.filter_by(id_offre=o.id_offre).all()
    for cot in all_cot:
        cot_tot += cot.budget
    o.cotisation = cot_tot
    if reponse:
        if f.validate_on_submit():
            reponse.desc_rep = f.autre_rep.data
            reponse.budget = f.cotisation_apportee.data
            reponse.date_debut = f.date_debut.data
            reponse.date_fin = f.date_fin.data
            reponse.capacite_salle = f.cap_salle.data
            db.session.commit()
            return redirect(url_for('reponses.mes_reponses'))
        f.autre_rep.data = reponse.desc_rep
        f.cotisation_apportee.data = reponse.budget
        f.date_debut.data = reponse.date_debut
        f.date_fin.data = reponse.date_fin
        f.cap_salle.data = reponse.capacite_salle
    else:
        if f.validate_on_submit():
            r = Reponse()
            r.desc_rep = f.autre_rep.data
            r.budget = f.cotisation_apportee.data
            r.id_utilisateur = current_user.id_utilisateur
            r.date_debut = f.date_debut.data
            r.date_fin = f.date_fin.data
            r.capacite_salle = f.cap_salle.data
            r.id_offre = o.id_offre
            db.session.add(r)
            db.session.commit()
            return redirect(url_for('reponses.mes_reponses'))
        f.cotisation_apportee.data = o.cotisation_min
        f.cap_salle.data = o.capacite_min
    return render_template('repondre-offre.html', offre=o, form=f)
