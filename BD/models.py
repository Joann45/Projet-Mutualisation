#!/ usr / bin / python3

import connexion
from sqlalchemy import MetaData
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

# Classe Offre
class Offre(Base):
    __tablename__ = 'OFFRE'

    id_offre = Column(Integer, primary_key=True)
    nom_offre = Column(Text)
    description = Column(Text)
    date_limite = Column(Date)
    budget = Column(Numeric)
    capacite_min = Column(Integer)
    capacite_max = Column(Integer)
    etat = Column(Text)

    id_orga = Column(Integer, ForeignKey('ORGANISATEUR.id_orga'))
    id_loc = Column(Integer, ForeignKey('LOCALISATION.id_loc'))
    id_plage = Column(Integer, ForeignKey('PLAGE_DATE.id_plage'))

    # Relations
    orga = relationship('Organisateur', back_populates='les_offres')
    loc = relationship('Localisation', back_populates='les_offres')
    date = relationship('PlageDate', back_populates='les_offres')

    les_documents = relationship('Document', back_populates='offre')

    les_genres = relationship('ContenirGenre', back_populates='offre')
    les_liens = relationship('ContenirLien', back_populates='offre')
    les_reponses_orgas = relationship('Repondre', back_populates='offre_orga')
    les_reseaux = relationship('PartagerOffre', back_populates='offre')

# Classe Genre
class Genre(Base):
    __tablename__ = 'GENRE'

    id_genre = Column(Integer, primary_key=True)
    nom_genre = Column(Text)

    les_offres = relationship('ContenirGenre', back_populates='genre')

# Classe Lien
class Lien(Base):
    __tablename__ = 'LIEN'

    id_lien = Column(Integer, primary_key=True)
    nom_lien = Column(Text)

    les_offres = relationship('ContenirLien', back_populates='lien')

# Classe Reseau
class Reseau(Base):
    __tablename__ = 'RESEAU'

    id_reseau = Column(Integer, primary_key=True)
    nom_reseau = Column(Text)
    id_admin = Column(Integer, ForeignKey('ADMINISTRATEUR.id_admin'))

    les_offres = relationship('PartagerOffre', back_populates='reseau')
    reseaux_orga = relationship('AppartenirOrga', back_populates='reseau')

    administrateur = relationship('Administrateur', back_populates='les_reseaux')

# Classe Administrateur
class Administrateur(Base):
    __tablename__ = 'ADMINISTRATEUR'

    id_admin = Column(Integer, primary_key=True)
    nom_admin = Column(Text)
    prenom_admin = Column(Text)
    mdp_admin = Column(Text)
    email_admin = Column(Text)

    les_reseaux = relationship('Reseau', back_populates='administrateur')

# Classe Document
class Document(Base):
    __tablename__ = 'DOCUMENT'

    id_doc = Column(Integer, primary_key=True)
    nom_doc = Column(Text)
    details_doc = Column(Text)

    id_offre = Column(Integer, ForeignKey('OFFRE.id_offre'))

    offre = relationship('Offre', back_populates='les_documents')

# Classe Organisateur
class Organisateur(Base):
    __tablename__ = 'ORGANISATEUR'

    id_orga = Column(Integer, primary_key=True)
    nom_orga = Column(Text)
    prenom_orga = Column(Text)
    mdp_orga = Column(Text)
    email_orga = Column(Text)

    les_offres = relationship('Offre', back_populates='orga')
    orgas_offre = relationship('Repondre', back_populates='orga')
    orgas_reseau = relationship('AppartenirOrga', back_populates='orga')

# Classe Localisation
class Localisation(Base):
    __tablename__ = 'LOCALISATION'

    id_loc = Column(Integer, primary_key=True)
    nom_loc = Column(Text)

    les_offres = relationship('Offre', back_populates='loc')

# Classe PlageDate
class PlageDate(Base):
    __tablename__ = 'PLAGE_DATE'

    id_plage = Column(Integer, primary_key=True)
    date_deb = Column(Date)
    date_fin = Column(Date)

    les_offres = relationship('Offre', back_populates='date')

# Classe ContenirGenre (table d'association entre Offre et Genre)
class ContenirGenre(Base):
    __tablename__ = 'CONTENIRGENRE'

    id_genre = Column(Integer, ForeignKey('GENRE.id_genre'), primary_key=True)
    id_offre = Column(Integer, ForeignKey('OFFRE.id_offre'), primary_key=True)

    genre = relationship("Genre", back_populates="les_offres")
    offre = relationship("Offre", back_populates="les_genres")

# Classe ContenirLien (table d'association entre Offre et Lien)
class ContenirLien(Base):
    __tablename__ = 'CONTENIRLIEN'

    id_lien = Column(Integer, ForeignKey('LIEN.id_lien'), primary_key=True)
    id_offre = Column(Integer, ForeignKey('OFFRE.id_offre'), primary_key=True)

    lien = relationship("Lien", back_populates="les_offres")
    offre = relationship("Offre", back_populates="les_liens")

# Classe Repondre (table d'association entre Organisateur et Offre)
class Repondre(Base):
    __tablename__ = 'REPONDRE'

    id_orga = Column(Integer, ForeignKey('ORGANISATEUR.id_orga'), primary_key=True)
    id_offre = Column(Integer, ForeignKey('OFFRE.id_offre'), primary_key=True)
    desc_rep = Column(Text)

    orga = relationship("Organisateur", back_populates="orgas_offre")
    offre_orga = relationship("Offre", back_populates="les_reponses_orgas")

# Classe AppartenirOrga (table d'association entre Organisateur et Reseau)
class AppartenirOrga(Base):
    __tablename__ = 'APPARTENIRORGA'

    id_orga = Column(Integer, ForeignKey('ORGANISATEUR.id_orga'), primary_key=True)
    id_reseau = Column(Integer, ForeignKey('RESEAU.id_reseau'), primary_key=True)

    orga = relationship("Organisateur", back_populates="orgas_reseau")
    reseau = relationship("Reseau", back_populates="reseaux_orga")

# Classe PartagerOffre (table d'association entre Offre et Reseau)
class PartagerOffre(Base):
    __tablename__ = 'PARTAGEROFFRE'

    id_offre = Column(Integer, ForeignKey('OFFRE.id_offre'), primary_key=True)
    id_reseau = Column(Integer, ForeignKey('RESEAU.id_reseau'), primary_key=True)

    offre = relationship("Offre", back_populates="les_reseaux")
    reseau = relationship("Reseau", back_populates="les_offres")

if __name__ == '__main__':

    # Pour une connexion MySQL, utilisez le code ci-dessous (décommentez et remplissez les informations)
    engine = connexion.ouvrir_connexion('raignault', 'raignault', 'servinfo-maria', 'DBraignault')

    # Création de la connexion qui fait le lien entre notre script et la BD
    cnx = engine.connect()

    # Création d'un objet MetaData pour introspecter les tables
    metadata = MetaData()
    metadata.reflect(bind=engine)

    print("--- Suppression de toutes les tables de la BD ---")
    Base.metadata.drop_all(bind=engine)

    print("--- Construction des tables de la BD ---")
    Base.metadata.create_all(bind=engine)

    # Afficher les noms des tables
    print("Tables dans la base de données :", metadata.tables.keys())
