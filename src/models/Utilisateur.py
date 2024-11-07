from src.app import db, login_manager
from flask_security import UserMixin
import uuid

# Classe Utilisateur
class Utilisateur(db.Model, UserMixin):
    __tablename__ = 'UTILISATEUR'

    id_utilisateur = db.Column(db.Integer, primary_key=True)
    nom_utilisateur = db.Column(db.Text)
    prenom_utilisateur = db.Column(db.Text)
    mdp_utilisateur = db.Column(db.Text)
    email_utilisateur = db.Column(db.Text, unique=True)
    img_utilisateur = db.Column(db.Text)
    role_id = db.Column(db.Integer, db.ForeignKey('ROLE.id_role'))
    active = db.Column(db.Boolean, default=True)
    fs_uniquifier = db.Column(db.String(255), unique=True, default=lambda: str(uuid.uuid4()))  # Ajoutez cette ligne

    
    les_notifs = db.relationship('Notification_Utilisateur', back_populates='utilisateur', lazy=True) 
    les_offres = db.relationship('Offre', back_populates='utilisateur', lazy=True)
    les_reponses_offre = db.relationship('Reponse', back_populates='utilisateur', lazy=True)
    les_reseaux = db.relationship('Utilisateur_Reseau', back_populates='orga', lazy=True)