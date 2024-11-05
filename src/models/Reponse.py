from src.app import db

# Classe Reponse (table d'association)
class Reponse(db.Model):
    __tablename__ = 'REPONSE'

    id_orga = db.Column(db.Integer, db.ForeignKey('ORGANISATEUR.id_orga'), primary_key=True)
    id_offre = db.Column(db.Integer, db.ForeignKey('OFFRE.id_offre'), primary_key=True)
    desc_rep = db.Column(db.Text)

    orga = db.relationship("Organisateur", back_populates="orgas_offre", lazy=True)
    offre_orga = db.relationship("Offre", back_populates="les_reponses_orgas", lazy=True)