from src.app import db

# Classe Notification
class Notification(db.Model):
    __tablename__ = 'NOTIFICATION'

    id_notif = db.Column(db.Integer, primary_key=True)
    type_operation = db.Column(db.Text)
    date_notification = db.Column(db.Date)

    les_notifs_admin = db.relationship('NotifierAdmin', back_populates='notif', lazy=True)
    les_notifs_orga = db.relationship('NotifierOrga', back_populates='notif', lazy=True)