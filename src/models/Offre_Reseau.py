from src.app import db

# Classe Offre_Reseau (table d'association)
class Offre_Reseau(db.Model):
    __tablename__ = 'OFFRE_RESEAU'

    id_offre = db.Column(db.Integer, db.ForeignKey('OFFRE.id_offre'), primary_key=True)
    id_reseau = db.Column(db.Integer, db.ForeignKey('RESEAU.id_reseau'), primary_key=True)

    offre = db.relationship("Offre", back_populates="les_reseaux", lazy=True )
    reseau = db.relationship("Reseau", back_populates="les_offres", lazy=True)