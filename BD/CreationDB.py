#!/ usr / bin / python3

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Text, Date, Numeric
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy import func
import time
from datetime import date

from sqlalchemy.orm import registry
mapper_registry = registry()
Base = mapper_registry.generate_base()

from sqlalchemy import select
from sqlalchemy.orm import Session

class Genre(Base):
    __tablename__ = 'GENRE'

    id_genre = Column(Integer, primary_key = True)
    nom_genre = Column(Text)

    def __init__(self, id_genre, nom_genre):
        self.id_genre = id_genre
        self.nom_genre = nom_genre

class Localisation(Base):
    __tablename__ = 'LOCALISATION'

    id_loc = Column(Integer, primary_key = True)
    nom_loc = Column(Text)

    def __init__(self, id_loc, nom_loc):
        self.id_loc = id_loc
        self.nom_loc = nom_loc

class PlageDate(Base):
    __tablename__ = 'PLAGE_DATE'

    id_plage = Column(Integer, primary_key = True)
    date_deb = Column(Date)
    date_fin = Column(Date)

    def __init__(self, id_plage, date_deb, date_fin):
        self.id_plage = id_plage
        self.date_deb = date_deb
        self.date_fin = date_fin

class Lien(Base):
    __tablename__ = 'LIEN'

    id_lien = Column(Integer, primary_key = True)
    nom_lien = Column(Text) 

    def __init__(self, id_lien, nom_lien):
        self.id_lien = id_lien
        self.nom_lien = nom_lien

class ContenirGenre(Base):
    __tablename__ = 'CONTENIRGENRE'

    id_genre = Column(Integer, ForeignKey('GENRE.id_genre'), primary_key = True)
    genre = relationship("Genre", back_populates = "lesgenres")
    id_offre = Column(Integer, ForeignKey('OFFRE.id_offre'), primary_key = True)
    offre = relationship("Offre", back_populates = "lesoffres")

    def __init__(self, id_genre, id_offre):
        self.id_genre = id_genre
        self.id_offre = id_offre 

class ContenirLocalisation(Base):
    __tablename__ = 'CONTENIRLOCALISATION'

    id_loc = Column(Integer, ForeignKey('LOCALISATION.id_loc'), primary_key = True)
    localisation = relationship("Localisation", back_populates = "leslocs")
    id_offre = Column(Integer, ForeignKey('OFFRE.id_offre'), primary_key = True)
    offre = relationship("Offre", back_populates = "lesoffres")

    def __init__(self, id_loc, id_offre):
        self.id_loc = id_loc
        self.id_offre = id_offre

class ContenirDate(Base):
    __tablename__ = 'CONTENIRDATE'

    id_plage = Column(Integer, ForeignKey('PLAGE_DATE.id_plage'), primary_key = True)
    plage_date = relationship("PlageDate", back_populates = "lesplages")
    id_offre = Column(Integer, ForeignKey('OFFRE.id_offre'), primary_key = True)
    offre = relationship("Offre", back_populates = "lesoffres")

    def __init__(self, id_plage, id_offre):
        self.id_plage = id_plage
        self.id_offre = id_offre

class ContenirLien(Base):
    __tablename__ = 'CONTENIRLIEN'

    id_lien = Column(Integer, ForeignKey('LIEN.id_lien'), primary_key = True)
    lien = relationship("Lien", back_populates = "lesliens")
    id_offre = Column(Integer, ForeignKey('OFFRE.id_offre'), primary_key = True)
    offre = relationship("Offre", back_populates = "lesoffres")

    def __init__(self, id_lien, id_offre):
        self.id_lien = id_lien
        self.id_offre = id_offre

class Offre(Base):
    __tablename__ = 'OFFRE'

    id_offre = Column(Integer, primary_key = True)
    nom_offre = Column(Text)
    artiste = Column(Text)
    description = Column(Text)
    date_limite = Column(Date)
    budget = Column(Numeric)
    capacite_min = Column(Integer)
    capacite_max = Column(Integer)
    etat = Column(Text)

    def __init__(self, id_offre, nom_offre, artiste, description, date_limite, budget, capacite_min, capacite_max, etat):
        self.id_offre = id_offre
        self.nom_offre = nom_offre
        self.artiste = artiste
        self.description = description
        self.date_limite = date_limite
        self.budget = budget
        self.capacite_min = capacite_min
        self.capacite_max = capacite_max
        self.etat = etat

class Document(Base):
    __tablename__ = 'DOCUMENT'

    id_doc = Column(Integer, primary_key = True)
    nom_doc = Column(Text)
    details_doc = Column(Text)

    def __init__(self, id_doc, nom_doc, details_doc):
        self.id_doc = id_doc
        self.nom_doc = nom_doc
        self.details_doc = details_doc

class Organisateur(Base):
    __tablename__ = 'ORGANISATEUR'

    id_orga = Column(Integer, primary_key = True)
    nom_orga = Column(Text)
    prenom_orga = Column(Text)
    mdp_orga = Column(Text)
    email_orga = Column(Text)

    def __init__(self, id_orga, nom_orga, prenom_orga, mdp_orga, email_orga):
        self.id_orga = id_orga
        self.nom_orga = nom_orga
        self.prenom_orga = prenom_orga
        self.mdp_orga = mdp_orga
        self.email_orga = email_orga
    

class Reseau(Base):
    __tablename__ = 'RESEAU'

    id_reseau = Column(Integer, primary_key = True)
    nom_reseau = Column(Text)

    def __init__(self, id_reseau, nom_reseau):
        self.id_reseau = id_reseau
        self.nom_reseau = nom_reseau

class AppartenirOrga(Base):
    __tablename__ = 'APPARTENIRORGA'

    id_orga = Column(Integer, ForeignKey('ORGANISATEUR.id_orga'), primary_key = True)
    organisateur = relationship("Organisateur", back_populates = "lesorgas")
    id_reseau = Column(Integer, ForeignKey('REASEAU.id_reseau'), primary_key = True)
    reseau = relationship("Reseau", back_populates = "lesreseaux")

    def __init__(self, id_orga, id_reseau):
        self.id_orga = id_orga
        self.id_reseau = id_reseau

class PartagerOffre(Base):
    __tablename__ = 'PARTAGEROFFRE'

    id_offre = Column(Integer, ForeignKey('OFFRE.id_offre'), primary_key = True)
    offre = relationship("Offre", back_populates = "lesoffres")
    id_reseau = Column(Integer, ForeignKey('REASEAU.id_reseau'), primary_key = True)
    reseau = relationship("Reseau", back_populates = "lesreseaux")

    def __init__(self, id_offre, id_reseau):
        self.id_offre = id_offre
        self.id_reseau = id_reseau

class Administrateur(Base):
    __tablename__ = 'ADMINISTRATEUR'

    id_admin = Column(Integer, primary_key = True)
    nom_admin = Column(Text)
    prenom_admin = Column(Text)
    mdp_admin = Column(Text)
    email_admin = Column(Text)

    def __init__(self, id_admin, nom_admin, prenom_admin, mdp_admin, email_admin):
        self.id_admin = id_admin
        self.nom_admin = nom_admin
        self.prenom_admin = prenom_admin
        self.mdp_admin = mdp_admin
        self.email_admin = email_admin
