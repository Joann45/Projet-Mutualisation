from sqlalchemy.orm import sessionmaker
from models import *
import unittest
from datetime import date

ENGINE = connexion.ouvrir_connexion('raignault', 'raignault', 'servinfo-maria', 'DBraignault')
Session = sessionmaker(bind=ENGINE)
SESSION = Session()

def insertions():
    # Insertion dans la table Organisateur
    organisateur1 = Organisateur(
        nom_orga="Dupont",
        prenom_orga="Jean",
        mdp_orga="password123",
        email_orga="jean.dupont@gmail.com"
    )
    SESSION.add(organisateur1)

    # Insertion dans la table Localisation
    localisation1 = Localisation(
        nom_loc="Paris"
    )
    SESSION.add(localisation1)

    # Insertion dans la table PlageDate
    plage_date1 = PlageDate(
        date_deb=date(2024, 10, 20),
        date_fin=date(2024, 10, 25)
    )
    SESSION.add(plage_date1)

    # Insertion dans la table Genre
    genre1 = Genre(
        nom_genre="Rock"
    )
    SESSION.add(genre1)

    # Insertion dans la table Lien
    lien1 = Lien(
        nom_lien="YouTube.com"
    )
    SESSION.add(lien1)

    # Insertion dans la table Offre
    offre1 = Offre(
        nom_offre="Concert de Rock",
        description="Un concert de rock en plein air.",
        date_limite=date(2024, 10, 18),
        budget=15000.00,
        capacite_min=100,
        capacite_max=500,
        etat="En attente",
        orga=organisateur1,
        loc=localisation1,
        date=plage_date1
    )
    SESSION.add(offre1)

    # Insertion dans la table Document
    document1 = Document(
        nom_doc="Plan du Concert",
        details_doc="Plan détaillé des emplacements et des accès.",
        offre=offre1
    )
    SESSION.add(document1)

    # Insertion dans la table Administrateur
    admin1 = Administrateur(
        nom_admin="Martin",
        prenom_admin="Paul",
        mdp_admin="admin123",
        email_admin="paul.martin@example.com"
    )
    SESSION.add(admin1)

    # Insertion dans la table Réseau
    reseau1 = Reseau(
        nom_reseau="Centre-Val de Loire",
        administrateur=admin1
    )
    SESSION.add(reseau1)

    # Insertion dans la table association Appartenir Orga
    appartenir_orga = AppartenirOrga(
        orga=organisateur1,
        reseau=reseau1
    )
    SESSION.add(appartenir_orga)

    # Insertion dans la table association Partager Offre
    partager_offre = PartagerOffre(
        offre=offre1,
        reseau=reseau1
    )
    SESSION.add(partager_offre)

    # Validation des changements (insertion des données dans la BD)
    SESSION.commit()