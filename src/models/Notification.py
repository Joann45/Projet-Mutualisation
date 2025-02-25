from src.extensions import db

# Classe Notification
class Notification(db.Model):
    __tablename__ = 'NOTIFICATION'

    id_notif = db.Column(db.Integer, primary_key=True)
    type_operation = db.Column(db.Text)
    date_notification = db.Column(db.Date)
    expediteur = db.Column(db.Text)

    les_notifs = db.relationship('Notification_Utilisateur', back_populates='notif', lazy=True)