import sys
import os
import unittest

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.append(os.path.join(ROOT, 'BD'))

from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
import BD.insertions_data_test as data
import models
import connexion

# Ouverture de la connexion à la base de données
ENGINE = connexion.ouvrir_connexion('raignault', 'raignault', 'servinfo-maria', 'DBraignault')
Session = sessionmaker(bind=ENGINE)
SESSION = Session()

Base = models.get_base()

# Désactivation des contraintes de clé étrangère
SESSION.execute(text("SET FOREIGN_KEY_CHECKS = 0"))

tables = [table for table in Base.metadata.tables]

# Boucle de suppression des données table par table
for table in tables:
    print(table)
    SESSION.execute(text(f"DELETE FROM {table}"))

# Réactivation des contraintes de clé étrangère
SESSION.execute(text("SET FOREIGN_KEY_CHECKS = 1"))

# Valider les changements
SESSION.commit()

# Insertion initiale pour les tests
data.insertions(data.ORGA, data.NOTIF, data.LOC, data.PLAGE_DATE, data.GENRE, data.LIEN, data.OFFRE, data.DOC, data.ADMIN, data.RESEAU, data.APPARTENIR_ORGA, data.PARTAGER_OFFRE, data.NOTIF_ADMIN, data.NOTIF_ORGA)

class TestDatabaseOperations(unittest.TestCase):

    def test_insert_organisateur(self):
        organisateur = SESSION.query(models.Organisateur).get(data.ORGA.id_orga)
        self.assertIsNotNone(organisateur)
        self.assertEqual(organisateur.prenom_orga, data.ORGA.prenom_orga)
        self.assertEqual(organisateur.email_orga, data.ORGA.email_orga)

    def test_insert_localisation(self):
        localisation = SESSION.query(models.Localisation).get(data.LOC.id_loc)
        self.assertIsNotNone(localisation)
        self.assertEqual(localisation.nom_loc, data.LOC.nom_loc)

    def test_insert_plage_date(self):
        plage = SESSION.query(models.PlageDate).get(data.PLAGE_DATE.id_plage)
        self.assertIsNotNone(plage)
        self.assertEqual(plage.date_fin, data.PLAGE_DATE.date_fin)

    def test_insert_genre(self):
        genre = SESSION.query(models.Genre).get(data.GENRE.id_genre)
        self.assertIsNotNone(genre)
        self.assertEqual(genre.nom_genre, data.GENRE.nom_genre)

    def test_insert_lien(self):
        lien = SESSION.query(models.Lien).get(data.LIEN.id_lien)
        self.assertIsNotNone(lien)
        self.assertEqual(lien.nom_lien, data.LIEN.nom_lien)

    def test_insert_offre(self):
        offre = SESSION.query(models.Offre).get(data.OFFRE.id_offre)
        self.assertIsNotNone(offre)
        self.assertEqual(offre.description, data.OFFRE.description)
        self.assertEqual(offre.etat, data.OFFRE.etat)

    def test_insert_document(self):
        document = SESSION.query(models.Document).get(data.DOC.id_doc)
        self.assertIsNotNone(document)
        self.assertEqual(document.details_doc, data.DOC.details_doc)

    def test_insert_administrateur(self):
        admin = SESSION.query(models.Administrateur).get(data.ADMIN.id_admin)
        self.assertIsNotNone(admin)
        self.assertEqual(admin.prenom_admin, data.ADMIN.prenom_admin)

    def test_insert_reseau(self):
        reseau = SESSION.query(models.Reseau).get(data.RESEAU.id_reseau)
        self.assertIsNotNone(reseau)
        self.assertEqual(reseau.administrateur.nom_admin, data.ADMIN.nom_admin)

    def test_insert_appartenir_orga(self):
        relation = SESSION.query(models.AppartenirOrga).filter_by(id_orga=data.ORGA.id_orga, id_reseau=data.RESEAU.id_reseau).first()
        self.assertIsNotNone(relation)

    def test_insert_partager_offre(self):
        relation = SESSION.query(models.PartagerOffre).filter_by(id_offre=data.OFFRE.id_offre, id_reseau=data.RESEAU.id_reseau).first()
        self.assertIsNotNone(relation)

    def test_notifier_admin_insertion(self):
        notif_admin = SESSION.query(models.NotifierAdmin).filter_by(id_admin=data.ADMIN.id_admin, id_notif=data.NOTIF.id_notif).first()
        self.assertIsNotNone(notif_admin)
        self.assertEqual(notif_admin.notif.type_operation, data.NOTIF.type_operation)

    def test_notifier_orga_insertion(self):
        notif_orga = SESSION.query(models.NotifierOrga).filter_by(id_orga=data.ORGA.id_orga, id_notif=data.NOTIF.id_notif).first()
        self.assertIsNotNone(notif_orga)
        self.assertEqual(notif_orga.notif.type_operation, data.NOTIF.type_operation)

    def tearDown(self):
        # Nettoyer la base de données après chaque test
        SESSION.rollback()

# Fermez la session après la création des tests
SESSION.close()
