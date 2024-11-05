#!/usr/bin/python3

from src.app import db

# Classe Notification_Orga (table d'association)
class Notification_Orga(db.Model):
    __tablename__ = 'NOTIFICATION_ORGA'

    id_orga = db.Column(db.Integer, db.ForeignKey('ORGANISATEUR.id_orga'), primary_key=True)
    id_notif = db.Column(db.Integer, db.ForeignKey('NOTIFICATION.id_notif'), primary_key=True)

    orga = db.relationship("Organisateur", back_populates="les_notifs", lazy=True)
    notif = db.relationship("Notification", back_populates="les_notifs_orga", lazy=True)
