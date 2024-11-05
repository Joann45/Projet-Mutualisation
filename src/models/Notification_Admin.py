from src.app import db

# Classe Notification_Admin (table d'association)
class Notification_Admin(db.Model):
    __tablename__ = 'NOTIFICATION_ADMIN'

    id_admin = db.Column(db.Integer, db.ForeignKey('ADMINISTRATEUR.id_admin'), primary_key=True)
    id_notif = db.Column(db.Integer, db.ForeignKey('NOTIFICATION.id_notif'), primary_key=True)

    admin = db.relationship("Administrateur", back_populates="les_notifs", lazy=True)
    notif = db.relationship("Notification", back_populates="les_notifs_admin", lazy=True)