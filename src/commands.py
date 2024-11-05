import click
from .app import app, db

@app.cli.command()
@click.argument('filename')
def loaddb(filename):
    '''Creates the tables and populates them with data.'''
    # Création de toutes les tables
    db.create_all()
    
    # Import des modèles
    import src.models.models as md
    import yaml
    
    with open(filename, 'r') as file:
        data = yaml.safe_load(file)

    elements = {
        'organisateur': {},
        'administrateur': {},
        'reseau': {},
        'document': {},
        'notification': {},
        'genre': {},
        'lien': {},
        'localisation': {},
        'offre': {},
        'plage_date': {},
        'appartenir_orga': {},
        'contenir_genre': {},
        'contenir_liens': {},
        'partager_offre': {},
        'repondre': {},
        'notifier_admin': {},
        'notifier_orga': {}
    }

    for elem in data:
        if elem["type"] == "organisateur":
            organisateur = md.Organisateur(
                id_orga=elem["id_orga"],
                nom_orga=elem["nom_orga"],
                prenom_orga=elem["prenom_orga"],
                mdp_orga=elem["mdp_orga"],
                email_orga=elem["email_orga"],
                img_orga=elem["img_orga"]
            )
            elements["organisateur"][elem["id_orga"]] = organisateur
            db.session.add(organisateur)

        elif elem["type"] == "administrateur":
            administrateur = md.Administrateur(
                id_admin=elem["id_admin"],
                nom_admin=elem["nom_admin"],
                prenom_admin=elem["prenom_admin"],
                mdp_admin=elem["mdp_admin"],
                email_admin=elem["email_admin"],
                img_admin=elem["img_admin"]
            )
            elements["administrateur"][elem["id_admin"]] = administrateur
            db.session.add(administrateur)

        elif elem["type"] == "reseau":
            reseau = md.Reseau(
                id_reseau=elem["id_reseau"],
                nom_reseau=elem["nom_reseau"],
                id_admin=elem["id_admin"]
            )
            elements["reseau"][elem["id_reseau"]] = reseau
            db.session.add(reseau)

        elif elem["type"] == "document":
            document = md.Document(
                id_doc=elem["id_doc"],
                nom_doc=elem["nom_doc"],
                details_doc=elem["details_doc"],
                id_offre=elem["id_offre"]
            )
            elements["document"][elem["id_doc"]] = document
            db.session.add(document)

        elif elem["type"] == "notification":
            notification = md.Notification(
                id_notif=elem["id_notif"],
                type_operation=elem["type_operation"],
                date_notification=elem["date_notification"]
            )
            elements["notification"][elem["id_notif"]] = notification
            db.session.add(notification)

        elif elem["type"] == "genre":
            genre = md.Genre(
                id_genre=elem["id_genre"],
                nom_genre=elem["nom_genre"]
            )
            elements["genre"][elem["id_genre"]] = genre
            db.session.add(genre)

        elif elem["type"] == "lien":
            lien = md.Lien(
                id_lien=elem["id_lien"],
                nom_lien=elem["nom_lien"]
            )
            elements["lien"][elem["id_lien"]] = lien
            db.session.add(lien)

        elif elem["type"] == "localisation":
            localisation = md.Localisation(
                id_loc=elem["id_loc"],
                nom_loc=elem["nom_loc"]
            )
            elements["localisation"][elem["id_loc"]] = localisation
            db.session.add(localisation)

        elif elem["type"] == "offre":
            offre = md.Offre(
                id_offre=elem["id_offre"],
                nom_offre=elem["nom_offre"],
                description=elem["description"],
                date_limite=elem["date_limite"],
                budget=elem["budget"],
                capacite_min=elem["capacite_min"],
                capacite_max=elem["capacite_max"],
                etat=elem["etat"],
                id_orga=elem["id_orga"],
                id_loc=elem["id_loc"],
                id_plage=elem["id_plage"]
            )
            elements["offre"][elem["id_offre"]] = offre
            db.session.add(offre)

        elif elem["type"] == "plage_date":
            plage_date = md.PlageDate(
                id_plage=elem["id_plage"],
                date_deb=elem["date_deb"],
                date_fin=elem["date_fin"]
            )
            elements["plage_date"][elem["id_plage"]] = plage_date
            db.session.add(plage_date)

        elif elem["type"] == "appartenir_orga":
            appartenir_orga = md.AppartenirOrga(
                id_orga=elem["id_orga"],
                id_reseau=elem["id_reseau"]
            )
            elements["appartenir_orga"][(elem["id_orga"], elem["id_reseau"])] = appartenir_orga
            db.session.add(appartenir_orga)

        elif elem["type"] == "contenir_genre":
            contenir_genre = md.ContenirGenre(
                id_genre=elem["id_genre"],
                id_offre=elem["id_offre"]
            )
            elements["contenir_genre"][(elem["id_genre"], elem["id_offre"])] = contenir_genre
            db.session.add(contenir_genre)

        elif elem["type"] == "contenir_liens":
            contenir_liens = md.ContenirLien(
                id_lien=elem["id_lien"],
                id_offre=elem["id_offre"]
            )
            elements["contenir_liens"][(elem["id_lien"], elem["id_offre"])] = contenir_liens
            db.session.add(contenir_liens)

        elif elem["type"] == "partager_offre":
            partager_offre = md.PartagerOffre(
                id_offre=elem["id_offre"],
                id_reseau=elem["id_reseau"]
            )
            elements["partager_offre"][(elem["id_offre"], elem["id_reseau"])] = partager_offre
            db.session.add(partager_offre)

        elif elem["type"] == "repondre":
            repondre = md.Repondre(
                id_orga=elem["id_orga"],
                id_offre=elem["id_offre"],
                desc_rep=elem["desc_rep"]
            )
            elements["repondre"][(elem["id_orga"], elem["id_offre"])] = repondre
            db.session.add(repondre)

        elif elem["type"] == "notifier_admin":
            notifier_admin = md.NotifierAdmin(
                id_admin=elem["id_admin"],
                id_notif=elem["id_notif"]
            )
            elements["notifier_admin"][(elem["id_admin"], elem["id_notif"])] = notifier_admin
            db.session.add(notifier_admin)

        elif elem["type"] == "notifier_orga":
            notifier_orga = md.NotifierOrga(
                id_orga=elem["id_orga"],
                id_notif=elem["id_notif"]
            )
            elements["notifier_orga"][(elem["id_orga"], elem["id_notif"])] = notifier_orga
            db.session.add(notifier_orga)

    db.session.commit()
