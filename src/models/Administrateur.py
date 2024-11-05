from src.app import db

# Classe Administrateur
class Administrateur(db.Model):
    __tablename__ = 'ADMINISTRATEUR'

    id_admin = db.Column(db.Integer, primary_key=True)
    nom_admin = db.Column(db.Text)
    prenom_admin = db.Column(db.Text)
    mdp_admin = db.Column(db.Text)
    email_admin = db.Column(db.Text)
    img_admin = db.Column(db.Text)

    les_reseaux = db.relationship('Reseau', back_populates='administrateur', lazy=True)
    les_notifs = db.relationship('NotifierAdmin', back_populates='admin', lazy=True)