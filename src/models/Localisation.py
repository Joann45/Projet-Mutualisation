from src.app import db  # Assurez-vous que `db` est importé correctement depuis votre application

# Classe Localisation
class Localisation(db.Model):
    __tablename__ = 'LOCALISATION'

    id_loc = db.Column(db.Integer, primary_key=True)
    nom_loc = db.Column(db.Text)
    les_offres = db.relationship('Offre', back_populates='loc', lazy=True)