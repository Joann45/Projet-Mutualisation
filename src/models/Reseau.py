from src.app import db

# Classe Reseau
class Reseau(db.Model):
    __tablename__ = 'RESEAU'

    id_reseau = db.Column(db.Integer, primary_key=True)
    nom_reseau = db.Column(db.Text)
    id_admin = db.Column(db.Integer, db.ForeignKey('ADMINISTRATEUR.id_admin'))

    les_offres = db.relationship('Offre_Reseau', back_populates='reseau', lazy=True)
    reseaux_orga = db.relationship('Organisateur_Reseau', back_populates='reseau', lazy=True)
    administrateur = db.relationship('Administrateur', back_populates='les_reseaux', lazy=True)