from src.app import db

# Classe Reponse (table d'association)
class Reponse(db.Model):
    __tablename__ = 'REPONSE'

    id_utilisateur = db.Column(db.Integer, db.ForeignKey('UTILISATEUR.id_utilisateur'), primary_key=True)
    id_offre = db.Column(db.Integer, db.ForeignKey('OFFRE.id_offre'), primary_key=True)
    desc_rep = db.Column(db.Text)

    utilisateur = db.relationship("Utilisateur", back_populates="les_reponses_offre", lazy=True)
    offre = db.relationship("Offre", back_populates="les_reponses_utilisateurs", lazy=True)