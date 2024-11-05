#!/usr/bin/python3

from src.app import db


# Tables d'association
class ContenirGenre(db.Model):
    __tablename__ = 'CONTENIR_GENRE'

    id_genre = db.Column(db.Integer, db.ForeignKey('GENRE.id_genre'), primary_key=True)
    id_offre = db.Column(db.Integer, db.ForeignKey('OFFRE.id_offre'), primary_key=True)

    genre = db.relationship("Genre", back_populates="les_offres", lazy=True)
    offre = db.relationship("Offre", back_populates="les_genres", lazy=True)

class ContenirLien(db.Model):
    __tablename__ = 'CONTENIR_LIEN'

    id_lien = db.Column(db.Integer, db.ForeignKey('LIEN.id_lien'), primary_key=True)
    id_offre = db.Column(db.Integer, db.ForeignKey('OFFRE.id_offre'), primary_key=True)

    lien = db.relationship("Lien", back_populates="les_offres", lazy=True)
    offre = db.relationship("Offre", back_populates="les_liens", lazy=True)

class Repondre(db.Model):
    __tablename__ = 'REPONDRE'

    id_orga = db.Column(db.Integer, db.ForeignKey('ORGANISATEUR.id_orga'), primary_key=True)
    id_offre = db.Column(db.Integer, db.ForeignKey('OFFRE.id_offre'), primary_key=True)
    desc_rep = db.Column(db.Text)

    orga = db.relationship("Organisateur", back_populates="orgas_offre", lazy=True)
    offre_orga = db.relationship("Offre", back_populates="les_reponses_orgas", lazy=True)

class AppartenirOrga(db.Model):
    __tablename__ = 'APPARTENIR_ORGA'

    id_orga = db.Column(db.Integer, db.ForeignKey('ORGANISATEUR.id_orga'), primary_key=True)
    id_reseau = db.Column(db.Integer, db.ForeignKey('RESEAU.id_reseau'), primary_key=True)

    orga = db.relationship("Organisateur", back_populates="orgas_reseau", lazy=True)
    reseau = db.relationship("Reseau", back_populates="reseaux_orga", lazy=True)

class PartagerOffre(db.Model):
    __tablename__ = 'PARTAGER_OFFRE'

    id_offre = db.Column(db.Integer, db.ForeignKey('OFFRE.id_offre'), primary_key=True)
    id_reseau = db.Column(db.Integer, db.ForeignKey('RESEAU.id_reseau'), primary_key=True)

    offre = db.relationship("Offre", back_populates="les_reseaux", lazy=True)
    reseau = db.relationship("Reseau", back_populates="les_offres", lazy=True)

class NotifierAdmin(db.Model):
    __tablename__ = 'NOTIFIER_ADMIN'

    id_admin = db.Column(db.Integer, db.ForeignKey('ADMINISTRATEUR.id_admin'), primary_key=True)
    id_notif = db.Column(db.Integer, db.ForeignKey('NOTIFICATION.id_notif'), primary_key=True)

    admin = db.relationship("Administrateur", back_populates="les_notifs", lazy=True)
    notif = db.relationship("Notification", back_populates="les_notifs_admin", lazy=True)

class NotifierOrga(db.Model):
    __tablename__ = 'NOTIFIER_ORGA'

    id_orga = db.Column(db.Integer, db.ForeignKey('ORGANISATEUR.id_orga'), primary_key=True)
    id_notif = db.Column(db.Integer, db.ForeignKey('NOTIFICATION.id_notif'), primary_key=True)

    orga = db.relationship("Organisateur", back_populates="les_notifs", lazy=True)
    notif = db.relationship("Notification", back_populates="les_notifs_orga", lazy=True)
