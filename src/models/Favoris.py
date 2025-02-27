from src.extensions import db

class Favoris(db.Model):
    __tablename__ = 'FAVORIS'

    id_favoris = db.Column(db.Integer, primary_key=True)
    nom_offre = db.Column(db.Text)
    id_utilisateur = db.Column(db.Integer, db.ForeignKey('UTILISATEUR.id_utilisateur'))
    id_offre = db.Column(db.Integer, db.ForeignKey('OFFRE.id_offre'))

    offre = db.relationship('Offre', back_populates='les_favoris', lazy=True)
    utilisateur = db.relationship('Utilisateur', back_populates='les_favoris', lazy=True)
