from src.app import db

# Classe Lien_Offre (table d'association)
class Lien_Offre(db.Model):
    __tablename__ = 'LIEN_OFFRE'

    id_lien = db.Column(db.Integer, db.ForeignKey('LIEN.id_lien'), primary_key=True)
    id_offre = db.Column(db.Integer, db.ForeignKey('OFFRE.id_offre'), primary_key=True)

    lien = db.relationship("Lien", back_populates="les_offres", lazy=True)
    offre = db.relationship("Offre", back_populates="les_liens", lazy=True)