from src.app import db

# Classe Reseau
class Reseau(db.Model):
    __tablename__ = 'RESEAU'

    id_reseau = db.Column(db.Integer, primary_key=True)
    nom_reseau = db.Column(db.Text)

    les_offres = db.relationship('Offre_Reseau', back_populates='reseau', lazy=True, cascade="all, delete-orphan")
    les_utilisateurs = db.relationship('Utilisateur_Reseau', back_populates='reseau', lazy=True,  cascade="all, delete-orphan")
