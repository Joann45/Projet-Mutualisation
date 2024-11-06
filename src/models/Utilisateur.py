from src.app import db
from flask_security import UserMixin, RoleMixin

# Classe Utilisateur
class Utilisateur(db.Model, UserMixin):
    __tablename__ = 'UTILISATEUR'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.Text)
    prenom = db.Column(db.Text)
    mdp = db.Column(db.Text)
    email = db.Column(db.Text)
    img = db.Column(db.Text)
    role_id = db.Column(db.Integer, db.ForeignKey('ROLE.id_role'))
    
    # TODO : Ajouter les relations
    les_notifs = db.relationship('Notification_Utilisateur', back_populates='utilisateur', lazy=True) # ! Corriger les notifs
    les_offres = db.relationship('Offre', back_populates='utilisateur', lazy=True) # ! Les noms de tables
    les_reponses_offre = db.relationship('Reponse', back_populates='utilisateur', lazy=True) # ! Les noms de tables
    les_reseaux = db.relationship('Utilisateur_Reseau', back_populates='orga', lazy=True) # ! Les noms de tables
    
class Role(db.Model, RoleMixin):
    __tablename__ = 'ROLE'
    id_role = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    users = db.relationship('Utilisateur', backref='role')