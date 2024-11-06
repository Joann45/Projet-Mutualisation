import click
from .app import app, db
from .models.Utilisateur import Utilisateur
from .models.Role import Role

@app.cli.command()
@click.argument('filename')
def loaddb(filename):
    '''Creates the tables and populates them with data.'''
    # Création de toutes les tables
    db.create_all()
    
    # Import des modèles
    import src.models as md
    import yaml
    
    with open(filename, 'r') as file:
        data = yaml.safe_load(file)

    elements = {
        'utilisateur': {},
        'reseau': {},
        'document': {},
        'notification': {},
        'notification_utilisateur': {},
        'genre_offre': {},
        'genre': {},
        'lien': {},
        'offre': {},
        'offre_reseau': {},
        'utilisateur_reseau': {},
        'lien_offre': {},
        'reponse': {},
        'role': {}
    }

    for elem in data:
        if elem["type"] == "utilisateur":
            utilisateur = Utilisateur(
                id_utilisateur=elem["id_utilisateur"],
                nom_utilisateur=elem["nom_utilisateur"],
                prenom_utilisateur=elem["prenom_utilisateur"],
                mdp_utilisateur=elem["mdp_utilisateur"],
                email_utilisateur=elem["email_utilisateur"],
                img_utilisateur=elem["img_utilisateur"],
                role_id=elem["role_id"]
            )
            elements["utilisateur"][elem["id_utilisateur"]] = utilisateur
            db.session.add(utilisateur)
            
        elif elem["type"] == "role":
            role = Role(
                id_role=elem["id_role"],
                name=elem["name"]
            )
            elements["role"][elem["id_role"]] = role
            db.session.add(role)

        elif elem["type"] == "offre_reseau":
            offre_reseau = md.Offre_Reseau(
                id_offre=elem["id_offre"],
                id_reseau=elem["id_reseau"]
            )
            elements["offre_reseau"][(elem["id_offre"], elem["id_reseau"])] = offre_reseau
            db.session.add(offre_reseau)

        elif elem["type"] == "reseau":
            reseau = md.Reseau(
                id_reseau=elem["id_reseau"],
                nom_reseau=elem["nom_reseau"],
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
            
        elif elem["type"] == "notification_utilisateur":
            notification_utilisateur = md.Notification_Utilisateur(
                id_utilisateur=elem["id_utilisateur"],
                id_notif=elem["id_notif"]
            )
            elements["notification_utilisateur"][(elem["id_utilisateur"], elem["id_notif"])] = notification_utilisateur
            db.session.add(notification_utilisateur)

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
                img=elem["img"],
                id_utilisateur=elem["id_utilisateur"],
                nom_loc=elem["nom_loc"],
                date_deb=elem["date_deb"],
                date_fin=elem["date_fin"]
            )
            elements["offre"][elem["id_offre"]] = offre
            db.session.add(offre)

        elif elem["type"] == "utilisateur_reseau":
            utilisateur_reseau = md.Utilisateur_Reseau(
                id_utilisateur=elem["id_utilisateur"],
                id_reseau=elem["id_reseau"]
            )
            elements["utilisateur_reseau"][(elem["id_utilisateur"], elem["id_reseau"])] = utilisateur_reseau
            db.session.add(utilisateur_reseau)

        elif elem["type"] == "genre_offre":
            genre_offre = md.Genre_Offre(
                id_genre=elem["id_genre"],
                id_offre=elem["id_offre"]
            )
            elements["genre_offre"][(elem["id_genre"], elem["id_offre"])] = genre_offre
            db.session.add(genre_offre)

        elif elem["type"] == "lien_offre":
            lien_offre = md.Lien_Offre(
                id_lien=elem["id_lien"],
                id_offre=elem["id_offre"]
            )
            elements["lien_offre"][(elem["id_lien"], elem["id_offre"])] = lien_offre
            db.session.add(lien_offre)
            
        elif elem["type"] == "reponse":
            reponse = md.Reponse(
                id_utilisateur=elem["id_utilisateur"],
                id_offre=elem["id_offre"],
                desc_rep=elem["desc_rep"]
            )
            elements["reponse"][(elem["id_utilisateur"], elem["id_offre"])] = reponse
            db.session.add(reponse)

    db.session.commit()

@app.cli.command()
def syncdb():
    '''Synchronizes the database.'''
    db.drop_all()
    db.create_all()
    db.session.commit()