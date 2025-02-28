from src.extensions import db

# Classe Favori
class Favori(db.Model):
    __tablename__ = 'FAVORI'

    id_favori = db.Column(db.Integer, primary_key=True)
    id_offre = db.Column(db.Integer, db.ForeignKey('OFFRE.id_offre'))
    id_utilisateur = db.Column(db.Integer, db.ForeignKey('UTILISATEUR.id_utilisateur'))

    offre = db.relationship('Offre', back_populates='les_favoris', lazy=True)
    utilisateur = db.relationship('Utilisateur', back_populates='les_favoris', lazy=True)
