from .app import app, db
from flask import render_template, redirect, url_for, request
from flask_security import login_required, current_user, roles_required,  logout_user, login_user
from src.forms.UtilisateurForm import InscriptionForm, ConnexionForm, UpdateUser, UpdatePassword
from flask import render_template, redirect, url_for, request, send_from_directory
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
            u.img_utilisateur = str(Utilisateur.get_last_id()+1)
            u.role_id = f.role.data
            file = f.img.data
            if file:
                file.save(os.path.join("src/static/img/profil", str(Utilisateur.get_last_id()+1)))
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



@app.route('/home/details-offre/<int:id_offre>', methods=['GET','POST'])
@login_required
def details_offre(id_offre):
    o = Offre.query.get(id_offre)
    commentaireForm = CommentaireForm()
    verif = False
    if commentaireForm.validate_on_submit():
        c = Commentaire()
        c.texte_commentaire = commentaireForm.texte_commentaire.data
        c.id_offre = id_offre
        c.id_utilisateur = current_user.id_utilisateur
        c.date_commentaire = datetime.now()
        db.session.add(c)
        db.session.commit()
        return redirect(url_for('details_offre', id_offre=id_offre))
    if not o:
        return redirect(url_for("home"))
    if Reponse.query.filter_by(id_utilisateur=current_user.id_utilisateur, id_offre=id_offre).first():
        verif = True
    return render_template('details-offre.html', offre=o, verif=verif, commentaireForm=commentaireForm)

@app.route('/home/repondre-offre/<int:id_offre>', methods=['GET','POST'])
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
    return render_template('repondre-offre.html', offre=o, form=f)

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
            file = f.img.data
            if file:
                file_path = os.path.join("src/static/img/profil", str(current_user.id_utilisateur))
                file.save(file_path)
            db.session.commit()
            return redirect(url_for('home'))
    f.nom_user.data = current_user.nom_utilisateur
    f.prenom_user.data = current_user.prenom_utilisateur
    f.email.data = current_user.email_utilisateur 
    return render_template('profil.html', form=f)



@app.route('/home/mes-reseaux', methods=['GET', 'POST'])
def mes_reseaux():
    """Renvoie la page des réseaux administrateur

    Returns:
        mes-reseaux-admin.html: Une page des réseaux pour un organisateur
    """
    f_select_reseau = SelectReseauForm()
    f_add_reseau = ReseauForm()
    add_user_form = AddUtilisateurReseauForm()

    # Récupérer les réseaux en fonction du rôle de l'utilisateur
    les_reseaux = get_reseaux_for_user(current_user)

    # Si aucun réseau n'est trouvé, afficher une page spécifique
    if not les_reseaux:
        return render_template('pas_reseau.html')

    # Définir les choix pour le formulaire de sélection de réseau
    f_select_reseau.reseaux.choices = [(reseau.id_reseau, reseau.nom_reseau) for reseau in les_reseaux]

    # Gérer la soumission du formulaire de sélection de réseau
    if f_select_reseau.validate_on_submit():
        reseau_id = f_select_reseau.reseaux.data
        return redirect(url_for('mes_reseaux', reseau_id=reseau_id))

    # Déterminer le réseau sélectionné
    reseau_id = request.args.get('reseau_id', type=int) or les_reseaux[0].id_reseau
    f_select_reseau.reseaux.default = reseau_id
    f_select_reseau.process()

    # Récupérer le réseau sélectionné
    reseau = Reseau.query.get(reseau_id)

    # Définir les choix pour le formulaire d'ajout d'utilisateur au réseau
    add_user_form.utilisateur.choices = get_available_users_for_reseau(reseau)

    # Gérer la soumission du formulaire d'ajout de réseau
    if f_add_reseau.validate_on_submit():
        add_new_reseau(f_add_reseau)
        return redirect(url_for('mes_reseaux'))

    # Récupérer les offres associées au réseau sélectionné
    les_offres = Offre.query.filter(Offre.les_reseaux.any(id_reseau=reseau_id)).all()

    return render_template(
        'mes-reseaux-admin.html',
        add_user_form=add_user_form,
        reseaux=les_reseaux,
        add_form=f_add_reseau,
        select_form=f_select_reseau,
        membres=[[membre.orga for membre in reseau.les_utilisateurs]],
        reseau_id=reseau_id,
        offres=les_offres,
        reseau=reseau
    )

def get_reseaux_for_user(user):
    """Récupère les réseaux en fonction du rôle de l'utilisateur."""
    if user.is_admin():
        return Reseau.query.all()
    return Reseau.query.filter(Reseau.les_utilisateurs.any(id_utilisateur=user.id_utilisateur)).all()

def get_available_users_for_reseau(reseau):
    """Récupère les utilisateurs disponibles pour être ajoutés au réseau."""
    liste_utilisateurs = [utilisateur.id_utilisateur for utilisateur in reseau.les_utilisateurs]
    return [(utilisateur.id_utilisateur, utilisateur.nom_utilisateur) for utilisateur in Utilisateur.query.all() if utilisateur.id_utilisateur not in liste_utilisateurs]

def add_new_reseau(form):
    """Ajoute un nouveau réseau à la base de données."""
    r = Reseau()
    r.nom_reseau = form.nom_reseau.data
    db.session.add(r)
    db.session.commit()

@app.route('/home/suppression_reseau/<int:id_reseau>', methods=['GET'])
def suppression_reseau(id_reseau):
    """Supprime un réseau
    Args:
        id_reseau (int): L'identifiant du réseau
    Returns:
        mes-reseaux-admin.html: Une page des réseaux pour un organisateur
    """
    reseau = Reseau.query.get(id_reseau)
    if reseau:
        db.session.delete(reseau)
        db.session.commit()
    return redirect(url_for('mes_reseaux'))

@app.route('/home/mes-offres/suppression-offre/<int:id_offre>', methods=['GET', 'POST'])
def suppression_offre(id_offre):
    """Supprime une offre

    Args:
        id_offre (int): L'identifiant de l'offre à supprimer

    Returns:
        mes-offres.html: Une page des offres de l'utilisateur
    """
    o = Offre.query.get(id_offre)
    if o:
        Offre_Reseau.query.filter_by(id_offre=id_offre).delete()
        Genre_Offre.query.filter_by(id_offre=id_offre).delete()
        db.session.delete(o)
        db.session.commit()
    return redirect(url_for('mes_offres'))

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
    return redirect(url_for('mes_reseaux', reseau_id=id_reseau))

@app.route('/static/Documents/<int:id_d>-<int:id_o>', methods=['GET', 'POST'])
def get_documents(id_d, id_o):

    documents_folder = os.path.join("static", "Documents")
    file_name = Document.query.filter_by(id_doc=id_d).first()
    new_filename = f"{file_name.nom_doc}"
    print(file_name.nom_doc)
    return send_from_directory(
        documents_folder,
        str(id_d)+"-"+str(id_o),
        as_attachment=True,
        download_name=new_filename
    )

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
        return redirect(url_for('mes_reseaux'))
    form = AddUtilisateurReseauForm()
    liste_utilisateurs = [utilisateur.id_utilisateur for utilisateur in reseau.les_utilisateurs]
    form.utilisateur.choices = [(utilisateur.id_utilisateur, utilisateur.nom_utilisateur) for utilisateur in Utilisateur.query.all() if utilisateur.id_utilisateur not in liste_utilisateurs]
    if form.validate_on_submit():
        utilisateur_id = form.utilisateur.data
        utilisateur_reseau = Utilisateur_Reseau(id_reseau=id_reseau, id_utilisateur=utilisateur_id)
        db.session.add(utilisateur_reseau)
        db.session.commit()
        return redirect(url_for('mes_reseaux', reseau_id=id_reseau))
    return render_template('add-utilisateur-reseau.html', form=form, reseau=reseau)

@app.route('/home/rechercher/les-offres', methods=['GET', 'POST'])
@login_required
def rechercher():
    """_summary_

    Returns:
        _type_: _description_
    """

    
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
        #o.img = f.img.data
        o.etat = "brouillon"
        o.nom_loc = f.nom_loc.data
        o.date_deb = f.date_deb.data
        o.date_fin = f.date_fin.data
        o.id_utilisateur = current_user.id_utilisateur
        db.session.add(o)
        db.session.commit()
        id_offre = o.id_offre
        o.img = id_offre

        d = Document() # ! pour l'instant il n'y a qu'un document par offre. Si ça marche pas, remplacer f.documents.data par list(f.documents.data) ou [f.documents.data]
        file = f.documents.data
        filename = secure_filename(file.filename)
        d.nom_doc = filename
        file = f.documents.data
        d.id_offre = id_offre
        db.session.add(d)
        db.session.commit()
        if file:
            file_path = os.path.join("src/static/Documents", str(d.id_doc)+"-"+str(id_offre)) 
            file.save(file_path)
        
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

@app.route('/home/mes-offres/publication/<int:id_offre>', methods=['GET','POST'])
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
        o.etat = "publiée"
        db.session.commit()
    return redirect(url_for('mes_offres'))

@app.route('/home/mes-offres')
@login_required
@app.route('/home/mes-offres', methods=["POST","GET"])
def mes_offres():
    """Renvoie la page des offres de l'utilisateur

    Returns:
        mes-offres.html: Une page des offres de l'utilisateur
    """
    

    les_reseaux = Reseau.query.all()
    f_select_reseau = SelectRechercheOffreForm()
    f_select_reseau.reseaux.choices = [(reseau.id_reseau, reseau.nom_reseau) for reseau in les_reseaux]

    proximité_date = SelectDateProximité()
    proximité_date.proxi.choices = ["Plus Proche", "Moins Proche"]

    if proximité_date.proxi.data == None :
        proximité_date.proxi.default = "Plus Proche"
        proximité_date.process()

    id_reseaux_elu =  f_select_reseau.reseaux.data
    les_reseaux_elu = []


    proxi_elu = proximité_date.proxi.data

   
    if proximité_date.validate_on_submit() or f_select_reseau.validate_on_submit():
        if proxi_elu == "Plus Proche": 
                les_offres = Offre.query.filter_by(id_utilisateur=current_user.id_utilisateur).order_by(Offre.date_fin).all()
        else:
                les_offres = Offre.query.filter_by(id_utilisateur=current_user.id_utilisateur).order_by(Offre.date_fin.desc()).all()

        for r in id_reseaux_elu:
            les_reseaux_elu.append(f_select_reseau.reseaux.choices[int(r)-1][0])
    else:
        les_offres = Offre.query.filter_by(id_utilisateur=current_user.id_utilisateur).order_by(Offre.date_fin).all()

    if les_reseaux_elu != []:
        les_offres = filtrage_des_offrres_par_reseux(les_reseaux_elu, les_offres)
    return render_template('mes-offres.html', offres=les_offres,form=f_select_reseau,formd=proximité_date)

def filtrage_des_offrres_par_reseux(les_reseaux_elu, les_offres):
    offre_voulu = set()
    for offre in les_offres:
        for reseux_off in offre.les_reseaux:
            if reseux_off.id_reseau in les_reseaux_elu:
                offre_voulu.add(offre)
    return list(offre_voulu)

@app.route('/home/les-offres', methods=["POST","GET"])
def les_offres():
    """Renvoie la page des offres

    Returns:
        les-offres.html: Une page des offres
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
                les_offres = Offre.query.filter_by(etat="publiee").order_by(Offre.date_fin).all()
        else:
                les_offres = Offre.query.filter_by(etat="publiee").order_by(Offre.date_fin.desc()).all()

        for r in id_reseaux_elu:
            les_reseaux_elu.append(f_select_reseau.reseaux.choices[int(r)-1][0])
    else:
        les_offres = Offre.query.filter_by(etat="publiee").order_by(Offre.date_fin).all()


    if les_reseaux_elu != []:
        les_offres = filtrage_des_offrres_par_reseux(les_reseaux_elu, les_offres)

    

    return render_template('les-offres.html', offres=les_offres,form=f_select_reseau,formd=proximité_date)

@app.route('/home/offre_personnel/<int:id_offre>')
@login_required
def offre_personnel(id_offre):
    o = Offre.query.get(id_offre)
    f = ReponseForm(o)
    if not o:
        return redirect(url_for("home"))
    return render_template('visualiser-offre-personnel.html', offre=o, form=f)

@app.route('/home/visualiser-reponses-offre/<int:id_offre>') #! A MODIFIER QUAND LA PAGE DE L'OFFRE SERA CREEE
def visualiser_reponses_offre(id_offre):
    """Renvoie la page de visualisation des réponses aux offres

    Returns:
        visualiser-reponses-offre.html: Une page de visualisation des réponses aux offres
    """
    les_reponses = Reponse.query.filter_by(id_offre=id_offre)
    if not les_reponses:
        return render_template('visualiser-reponses-offre.html', reponses=None)    
    return render_template('visualiser-reponses-offre.html', reponses=les_reponses)

@app.route('/home/mes-offres/mes-reponses', methods=["POST","GET"])
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
        les_reponses = filtrage_des_reponses_par_reseux(les_reseaux_elu, les_reponses)

    return render_template('mes-reponses.html', reponses=les_reponses, form=f_select_reseau, formd=proximité_date)
    

   
    

def filtrage_des_reponses_par_reseux(les_reseaux_elu, les_reponses):
    rep_voulu = set()
    for rep in les_reponses:
        for reseux_off in rep.offre.les_reseaux:
            print(reseux_off.id_reseau)
            if reseux_off.id_reseau in les_reseaux_elu:
                rep_voulu.add(rep)
    return list(rep_voulu)

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

