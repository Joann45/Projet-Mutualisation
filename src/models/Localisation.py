from src.app import db

# Classe Localisation
class Localisation(db.Model):
    __tablename__ = 'LOCALISATION'

    id_loc = db.Column(db.Integer, primary_key=True)
    nom_loc = db.Column(db.Text)
    les_offres = db.relationship('Offre', back_populates='loc', lazy=True)