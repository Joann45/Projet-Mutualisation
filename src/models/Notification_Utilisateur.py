from src.extensions import db


# Classe Notification_Utilisateur (table d'association)
class Notification_Utilisateur(db.Model):
    __tablename__ = 'NOTIFICATION_UTILISATEUR'

    id_utilisateur = db.Column(db.Integer, db.ForeignKey('UTILISATEUR.id_utilisateur'), primary_key=True)
    id_notif = db.Column(db.Integer, db.ForeignKey('NOTIFICATION.id_notif'), primary_key=True)

    utilisateur = db.relationship("Utilisateur", back_populates="les_notifs", lazy=True)
    notif = db.relationship("Notification", back_populates="les_notifs", lazy=True)