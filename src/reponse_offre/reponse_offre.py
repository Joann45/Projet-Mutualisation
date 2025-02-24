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
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import os
from functools import wraps
from flask import abort

views_bp = Blueprint('views', __name__, template_folder='templates')

@views_bp.route('/home/visualiser-reponses-offre/<int:id_offre>') #! A MODIFIER QUAND LA PAGE DE L'OFFRE SERA CREEE
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
    return render_template('offre/visualiser-reponses-offre.html',verif=verif, offre=o, reponses=les_reponses)  

def filtrage_des_reponses_par_reseaux(les_reseaux_elu, les_reponses):
    rep_voulu = set()
    for rep in les_reponses:
        for reseux_off in rep.offre.les_reseaux:
            print(reseux_off.id_reseau)
            if reseux_off.id_reseau in les_reseaux_elu:
                rep_voulu.add(rep)
    return list(rep_voulu)


@views_bp.route('/home/mes-offres/mes-reponses', methods=["POST","GET"])
def mes_reponses():
    """Renvoie la page des réponses de l'utilisateur

    Returns:
        mes-reponses.html: Une page des réponses de l'utilisateur
    """
    les_reseaux = Reseau.query.all()
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
        if proxi_elu == "Plus Proche": 
                les_reponses = Reponse.query.filter_by(id_utilisateur=current_user.id_utilisateur).all()
        else:
                les_reponses = Reponse.query.filter_by(id_utilisateur=current_user.id_utilisateur).all()

        for r in id_reseaux_elu:
            les_reseaux_elu.append(f_select_reseau.reseaux.choices[int(r)-1][0])
    else:
        les_reponses = Reponse.query.filter_by(id_utilisateur=current_user.id_utilisateur).all()


    if les_reseaux_elu != []:
        les_reponses = filtrage_des_reponses_par_reseaux(les_reseaux_elu, les_reponses)

    return render_template('reponse_offre/mes-reponses.html', reponses=les_reponses, form=f_select_reseau, formd=proximité_date)
    


@views_bp.route('/home/repondre-offre/<int:id_offre>', methods=['GET','POST'])
@login_required
def repondre_offre(id_offre):
    o = Offre.query.get(id_offre)
    f = ReponseForm(o)
    if not o:
        return redirect(url_for("home"))
    reponse = Reponse.query.filter_by(id_utilisateur=current_user.id_utilisateur, id_offre=id_offre).first()
    if reponse:
        if f.validate_on_submit():
            reponse.desc_rep = f.autre_rep.data
            reponse.budget = f.cotisation_apportee.data
            reponse.date_debut = f.date_debut.data
            reponse.date_fin = f.date_fin.data
            reponse.capacite_salle = f.cap_salle.data
            db.session.commit()
            return redirect(url_for('mes_reponses'))
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
            return redirect(url_for('mes_reponses'))
        f.cotisation_apportee.data = o.cotisation_min
        f.cap_salle.data = o.capacite_min
    return render_template('reponse_offre/repondre-offre.html', offre=o, form=f)
