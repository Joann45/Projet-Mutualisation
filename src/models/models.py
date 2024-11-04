#!/usr/bin/python3

from src.app import db  # Assurez-vous que `db` est importé correctement depuis votre application


# Classe Offre
class Offre(db.Model):
    __tablename__ = 'OFFRE'

    id_offre = db.Column(db.Integer, primary_key=True)
    nom_offre = db.Column(db.Text)
    description = db.Column(db.Text)
    date_limite = db.Column(db.Date)
    budget = db.Column(db.Numeric)
    capacite_min = db.Column(db.Integer)
    capacite_max = db.Column(db.Integer)
    etat = db.Column(db.Text)

    id_orga = db.Column(db.Integer, db.ForeignKey('ORGANISATEUR.id_orga'))
    id_loc = db.Column(db.Integer, db.ForeignKey('LOCALISATION.id_loc'))
    id_plage = db.Column(db.Integer, db.ForeignKey('PLAGE_DATE.id_plage'))

    # Relations
    orga = db.relationship('Organisateur', backref=db.backref('les_offres', lazy=True))
    loc = db.relationship('Localisation', backref=db.backref('les_offres', lazy=True))
    date = db.relationship('PlageDate', backref=db.backref('les_offres', lazy=True))
    les_documents = db.relationship('Document', back_populates='offre', lazy=True)
    les_genres = db.relationship('ContenirGenre', back_populates='offre', lazy=True)
    les_liens = db.relationship('ContenirLien', back_populates='offre', lazy=True)
    les_reponses_orgas = db.relationship('Repondre', back_populates='offre_orga', lazy=True)
    les_reseaux = db.relationship('PartagerOffre', back_populates='offre', lazy=True)

# Classe Genre
class Genre(db.Model):
    __tablename__ = 'GENRE'

    id_genre = db.Column(db.Integer, primary_key=True)
    nom_genre = db.Column(db.Text)
    les_offres = db.relationship('ContenirGenre', back_populates='genre', lazy=True)

# Classe Lien
class Lien(db.Model):
    __tablename__ = 'LIEN'

    id_lien = db.Column(db.Integer, primary_key=True)
    nom_lien = db.Column(db.Text)
    les_offres = db.relationship('ContenirLien', back_populates='lien', lazy=True)

# Classe Reseau
class Reseau(db.Model):
    __tablename__ = 'RESEAU'

    id_reseau = db.Column(db.Integer, primary_key=True)
    nom_reseau = db.Column(db.Text)
    id_admin = db.Column(db.Integer, db.ForeignKey('ADMINISTRATEUR.id_admin'))

    les_offres = db.relationship('PartagerOffre', back_populates='reseau', lazy=True)
    reseaux_orga = db.relationship('AppartenirOrga', back_populates='reseau', lazy=True)
    administrateur = db.relationship('Administrateur', back_populates='les_reseaux', lazy=True)

# Classe Administrateur
class Administrateur(db.Model):
    __tablename__ = 'ADMINISTRATEUR'

    id_admin = db.Column(db.Integer, primary_key=True)
    nom_admin = db.Column(db.Text)
    prenom_admin = db.Column(db.Text)
    mdp_admin = db.Column(db.Text)
    email_admin = db.Column(db.Text)
    img_admin = db.Column(db.Text)

    les_reseaux = db.relationship('Reseau', back_populates='administrateur', lazy=True)
    les_notifs = db.relationship('NotifierAdmin', back_populates='admin', lazy=True)

# Classe Document
class Document(db.Model):
    __tablename__ = 'DOCUMENT'

    id_doc = db.Column(db.Integer, primary_key=True)
    nom_doc = db.Column(db.Text)
    details_doc = db.Column(db.Text)
    id_offre = db.Column(db.Integer, db.ForeignKey('OFFRE.id_offre'))
    offre = db.relationship('Offre', back_populates='les_documents', lazy=True)

# Classe Organisateur
class Organisateur(db.Model):
    __tablename__ = 'ORGANISATEUR'

    id_orga = db.Column(db.Integer, primary_key=True)
    nom_orga = db.Column(db.Text)
    prenom_orga = db.Column(db.Text)
    mdp_orga = db.Column(db.Text)
    email_orga = db.Column(db.Text)
    img_orga = db.Column(db.Text)

    les_offres = db.relationship('Offre', back_populates='orga', lazy=True)
    les_notifs = db.relationship('NotifierOrga', back_populates='orga', lazy=True)
    orgas_offre = db.relationship('Repondre', back_populates='orga', lazy=True)
    orgas_reseau = db.relationship('AppartenirOrga', back_populates='orga', lazy=True)

# Classe Localisation
class Localisation(db.Model):
    __tablename__ = 'LOCALISATION'

    id_loc = db.Column(db.Integer, primary_key=True)
    nom_loc = db.Column(db.Text)
    les_offres = db.relationship('Offre', back_populates='loc', lazy=True)

# Classe PlageDate
class PlageDate(db.Model):
    __tablename__ = 'PLAGE_DATE'

    id_plage = db.Column(db.Integer, primary_key=True)
    date_deb = db.Column(db.Date)
    date_fin = db.Column(db.Date)
    les_offres = db.relationship('Offre', back_populates='date', lazy=True)

# Classe Notification
class Notification(db.Model):
    __tablename__ = 'NOTIFICATION'

    id_notif = db.Column(db.Integer, primary_key=True)
    type_operation = db.Column(db.Text)
    date_notification = db.Column(db.Date)

    les_notifs_admin = db.relationship('NotifierAdmin', back_populates='notif', lazy=True)
    les_notifs_orga = db.relationship('NotifierOrga', back_populates='notif', lazy=True)

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
