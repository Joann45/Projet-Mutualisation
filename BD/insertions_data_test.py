from sqlalchemy.orm import sessionmaker
from models import *
import unittest
from datetime import date

ENGINE = connexion.ouvrir_connexion('raignault', 'raignault', 'servinfo-maria', 'DBraignault')
Session = sessionmaker(bind=ENGINE)
SESSION = Session()

ORGA = Organisateur(
    nom_orga="Dupont",
    prenom_orga="Jean",
    mdp_orga="password123",
    email_orga="jean.dupont@gmail.com",
    img_orga = "img1"
)

# Insertion dans la table Notification
NOTIF = Notification(
    type_operation = "Nouvelle mise à jour disponible",
    date_notification = date(2024, 10, 30)
)

# Insertion dans la table Localisation
LOC = Localisation(
    nom_loc="Paris"
)

# Insertion dans la table PlageDate
PLAGE_DATE = PlageDate(
    date_deb=date(2024, 10, 20),
    date_fin=date(2024, 10, 25)
)

# Insertion dans la table Genre
GENRE = Genre(
    nom_genre="Rock"
)

# Insertion dans la table Lien
LIEN = Lien(
    nom_lien="YouTube.com"
)

# Insertion dans la table Offre
OFFRE = Offre(
    nom_offre="Concert de Rock",
    description="Un concert de rock en plein air.",
    date_limite=date(2024, 10, 18),
    budget=15000.00,
    capacite_min=100,
    capacite_max=500,
    etat="En attente",
    orga=ORGA,
    loc=LOC,
    date=PLAGE_DATE
)

# Insertion dans la table Document
DOC = Document(
    nom_doc="Plan du Concert",
    details_doc="Plan détaillé des emplacements et des accès.",
    offre=OFFRE
)

# Insertion dans la table Administrateur
ADMIN = Administrateur(
    nom_admin="Martin",
    prenom_admin="Paul",
    mdp_admin="admin123",
    email_admin="paul.martin@example.com",
    img_admin = "img2"
)

# Insertion dans la table Réseau
RESEAU = Reseau(
    nom_reseau="Centre-Val de Loire",
    administrateur=ADMIN
)

# Insertion dans la table association Appartenir Orga
APPARTENIR_ORGA = AppartenirOrga(
    orga=ORGA,
    reseau=RESEAU
)

# Insertion dans la table association Partager Offre
PARTAGER_OFFRE = PartagerOffre(
    offre=OFFRE,
    reseau=RESEAU
)

# Association administrateur - notification
NOTIF_ADMIN = NotifierAdmin(
    admin=ADMIN,
    notif=NOTIF
)

# Association organisateur - notification
NOTIF_ORGA = NotifierOrga(
    orga=ORGA,
    notif=NOTIF
)

def insertions(Orga, Notif, Loc, Plage, Genre, Lien, Offre, Doc, Admin, Reseau, AppOrga, PartOffre, NotifAdmin, NotifOrga):
    # Insertion dans la table Organisateur
    SESSION.add(Orga)

    # Insertion dans la table Notification
    SESSION.add(Notif)

    # Insertion dans la table Localisation
    SESSION.add(Loc)

    # Insertion dans la table PlageDate
    SESSION.add(Plage)

    # Insertion dans la table Genre
    SESSION.add(Genre)

    # Insertion dans la table Lien
    SESSION.add(Lien)

    # Insertion dans la table Offre
    SESSION.add(Offre)

    # Insertion dans la table Document
    SESSION.add(Doc)

    # Insertion dans la table Administrateur
    SESSION.add(Admin)

    # Insertion dans la table Réseau
    SESSION.add(Reseau)
    SESSION.commit()

    # Insertion dans la table association Appartenir Orga
    SESSION.add(AppOrga)

    # Insertion dans la table association Partager Offre
    SESSION.add(PartOffre)

    # Association administrateur - notification
    SESSION.add(NotifAdmin)

    # Association organisateur - notification
    SESSION.add(NotifOrga)

    # Validation des changements (insertion des données dans la BD)
    SESSION.commit()