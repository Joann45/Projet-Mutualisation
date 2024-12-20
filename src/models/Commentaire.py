from src.app import db

# Classe Commentaire
class Commentaire(db.Model):
    __tablename__ = 'COMMENTAIRE'

    id_commentaire = db.Column(db.Integer, primary_key=True)
    texte_commentaire = db.Column(db.Text)
    date_commentaire = db.Column(db.DateTime)
    id_offre = db.Column(db.Integer, db.ForeignKey('OFFRE.id_offre'))
    id_utilisateur = db.Column(db.Integer, db.ForeignKey('UTILISATEUR.id_utilisateur'))
    
    offre = db.relationship('Offre', back_populates='les_commentaires', lazy=True)
    utilisateur = db.relationship('Utilisateur', back_populates='les_commentaires', lazy=True)
