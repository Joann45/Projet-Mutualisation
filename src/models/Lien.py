from src.app import db

# Classe Lien
class Lien(db.Model):
    __tablename__ = 'LIEN'

    id_lien = db.Column(db.Integer, primary_key=True)
    nom_lien = db.Column(db.Text)
    les_offres = db.relationship('Lien_Offre', back_populates='lien', lazy=True)