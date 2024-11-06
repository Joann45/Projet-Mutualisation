from src.app import db
from flask_security import UserMixin

# Classe Utilisateur
class Utilisateur(db.Model, UserMixin):
    __tablename__ = 'UTILISATEUR'

    id_utilisateur = db.Column(db.Integer, primary_key=True)
    nom_utilisateur = db.Column(db.Text)
    prenom_utilisateur = db.Column(db.Text)
    mdp_utilisateur = db.Column(db.Text)
    email_utilisateur = db.Column(db.Text)
    img_utilisateur = db.Column(db.Text)
    role_id = db.Column(db.Integer, db.ForeignKey('ROLE.id_role'))
    
    les_notifs = db.relationship('Notification_Utilisateur', back_populates='utilisateur', lazy=True) 
    les_offres = db.relationship('Offre', back_populates='utilisateur', lazy=True)
    les_reponses_offre = db.relationship('Reponse', back_populates='utilisateur', lazy=True)
    les_reseaux = db.relationship('Utilisateur_Reseau', back_populates='orga', lazy=True)