from src.app import db

# Classe Utilisateur_Reseau (table d'association)
class Utilisateur_Reseau(db.Model):
    __tablename__ = 'UTILISATEUR_RESEAU'

    id_orga = db.Column(db.Integer, db.ForeignKey('UTILISATEUR.id'), primary_key=True)
    id_reseau = db.Column(db.Integer, db.ForeignKey('RESEAU.id_reseau'), primary_key=True)

    orga = db.relationship("Utilisateur", back_populates="les_reseaux", lazy=True)
    reseau = db.relationship("Reseau", back_populates="les_utilisateurs", lazy=True)