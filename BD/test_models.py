import sys
import os
import unittest

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.append(os.path.join(ROOT, 'BD'))

from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
import BD.insertions_data_test as insertions_data_test
import models
from datetime import date
import connexion
from sqlalchemy.orm import sessionmaker

# Ouverture de la connexion à la base de données
ENGINE = connexion.ouvrir_connexion('raignault', 'raignault', 'servinfo-maria', 'DBraignault')
Session = sessionmaker(bind=ENGINE)
SESSION = Session()

Base = models.get_base()

Base.metadata.drop_all(bind=ENGINE)
Base.metadata.create_all(bind=ENGINE)

# Valider les changements
SESSION.commit()

# Insertion initiale pour les tests
insertions_data_test.insertions()

class TestDatabaseOperations(unittest.TestCase):

    def test_insert_organisateur(self):
        organisateurs = list(SESSION.query(models.Organisateur).filter_by(nom_orga="Dupont"))
        self.assertEqual(len(organisateurs), 1)
        self.assertEqual(organisateurs[0].prenom_orga, "Jean")
        self.assertEqual(organisateurs[0].email_orga, "jean.dupont@gmail.com")

    def test_insert_localisation(self):
        localisations = list(SESSION.query(models.Localisation).filter_by(nom_loc="Paris"))
        self.assertEqual(len(localisations), 1)
        self.assertEqual(localisations[0].nom_loc, "Paris")

    def test_insert_plage_date(self):
        plages = list(SESSION.query(models.PlageDate).filter_by(date_deb=date(2024, 10, 20)))
        self.assertEqual(len(plages), 1)
        self.assertEqual(plages[0].date_fin, date(2024, 10, 25))

    def test_insert_genre(self):
        genres = list(SESSION.query(models.Genre).filter_by(nom_genre="Rock"))
        self.assertEqual(len(genres), 1)
        self.assertEqual(genres[0].nom_genre, "Rock")

    def test_insert_lien(self):
        liens = list(SESSION.query(models.Lien).filter_by(nom_lien="YouTube.com"))
        self.assertEqual(len(liens), 1)
        self.assertEqual(liens[0].nom_lien, "YouTube.com")

    def test_insert_offre(self):
        offres = list(SESSION.query(models.Offre).filter_by(nom_offre="Concert de Rock"))
        self.assertEqual(len(offres), 1)
        self.assertEqual(offres[0].description, "Un concert de rock en plein air.")
        self.assertEqual(offres[0].etat, "En attente")

    def test_insert_document(self):
        documents = list(SESSION.query(models.Document).filter_by(nom_doc="Plan du Concert"))
        self.assertEqual(len(documents), 1)
        self.assertEqual(documents[0].details_doc, "Plan détaillé des emplacements et des accès.")

    def test_insert_administrateur(self):
        admins = list(SESSION.query(models.Administrateur).filter_by(nom_admin="Martin"))
        self.assertEqual(len(admins), 1)
        self.assertEqual(admins[0].prenom_admin, "Paul")

    def test_insert_reseau(self):
        reseaux = list(SESSION.query(models.Reseau).filter_by(nom_reseau="Centre-Val de Loire"))
        self.assertEqual(len(reseaux), 1)
        self.assertEqual(reseaux[0].administrateur.nom_admin, "Martin")  # Assurez-vous que vous comparez avec un attribut correct

    def test_insert_appartenir_orga(self):
        relations = list(SESSION.query(models.AppartenirOrga).filter_by(orga=SESSION.query(models.Organisateur).filter_by(nom_orga="Dupont")[0]))
        self.assertEqual(len(relations), 1)

    def test_insert_partager_offre(self):
        relations = list(SESSION.query(models.PartagerOffre).filter_by(offre=SESSION.query(models.Offre).filter_by(nom_offre="Concert de Rock")[0]))
        self.assertEqual(len(relations), 1)

    def tearDown(self):
        # Nettoyer la base de données après chaque test
        SESSION.rollback()

# Fermez la session après la création des tests
SESSION.close()
