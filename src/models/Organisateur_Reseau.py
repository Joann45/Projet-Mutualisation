from src.app import db

# Classe Organisateur_Reseau (table d'association)
class Organisateur_Reseau(db.Model):
    __tablename__ = 'ORGANISATEUR_RESEAU'

    id_orga = db.Column(db.Integer, db.ForeignKey('ORGANISATEUR.id_orga'), primary_key=True)
    id_reseau = db.Column(db.Integer, db.ForeignKey('RESEAU.id_reseau'), primary_key=True)

    orga = db.relationship("Organisateur", back_populates="orgas_reseau", lazy=True)
    reseau = db.relationship("Reseau", back_populates="reseaux_orga", lazy=True)