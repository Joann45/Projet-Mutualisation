from src.extensions import db, login_manager
from flask_security import UserMixin
import uuid

# Classe Utilisateur
class Utilisateur(db.Model, UserMixin):
    __tablename__ = 'UTILISATEUR'

    id_utilisateur = db.Column(db.Integer, primary_key=True)
    nom_utilisateur = db.Column(db.Text)
    prenom_utilisateur = db.Column(db.Text)
    mdp_utilisateur = db.Column(db.Text)
    email_utilisateur = db.Column(db.Text, unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey('ROLE.id_role'))
    active = db.Column(db.Boolean, default=True)
    fs_uniquifier = db.Column(db.String(255), unique=True, default=lambda: str(uuid.uuid4()))  # Ajoutez cette ligne
    img_utilisateur = db.Column(db.Integer)

    
    les_notifs = db.relationship('Notification_Utilisateur', back_populates='utilisateur', lazy=True) 
    les_offres = db.relationship('Offre', back_populates='utilisateur', lazy=True)
    les_reponses_offre = db.relationship('Reponse', back_populates='utilisateur', lazy=True)
    les_reseaux = db.relationship('Utilisateur_Reseau', back_populates='orga', lazy=True,  cascade="all, delete-orphan")
    les_commentaires = db.relationship('Commentaire', back_populates='utilisateur', lazy=True, cascade="all, delete-orphan")
    les_favoris = db.relationship('Favori', back_populates='utilisateur', lazy=True, cascade="all, delete-orphan")
    
    def is_admin(self):
        return self.role_id == 2
    
    def get_role(self):
        if self.role_id == 1:
            return "Organisateur"
        elif self.role_id == 2:
            return "Administrateur"
        return None

    def get_last_id():
        id = 0
        users = Utilisateur.query.all()
        for user in users:
            if user.id_utilisateur > id:
                id = user.id_utilisateur
        return id

