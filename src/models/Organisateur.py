from src.app import db

# Classe Organisateur
class Organisateur(db.Model):
    __tablename__ = 'ORGANISATEUR'

    id_orga = db.Column(db.Integer, primary_key=True)
    nom_orga = db.Column(db.Text)
    prenom_orga = db.Column(db.Text)
    mdp_orga = db.Column(db.Text)
    email_orga = db.Column(db.Text)
    img_orga = db.Column(db.Text)

    les_offres = db.relationship('Offre', back_populates='orga', lazy=True)
    les_notifs = db.relationship('NotifierOrga', back_populates='orga', lazy=True)
    orgas_offre = db.relationship('Repondre', back_populates='orga', lazy=True)
    orgas_reseau = db.relationship('AppartenirOrga', back_populates='orga', lazy=True)