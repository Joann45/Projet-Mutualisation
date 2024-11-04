from sqlalchemy import create_engine, MetaData
import pymysql  # Assurez-vous que le module est importé

def ouvrir_connexion(user, passwd, host, database):
    """
    Ouverture d'une connexion MySQL
    Paramètres :
    user (str) : le login MySQL de l'utilisateur
    passwd (str) : le mot de passe MySQL de l'utilisateur
    host (str) : le nom ou l'adresse IP de la machine hébergeant le serveur MySQL
    database (str) : le nom de la base de données à utiliser

    Résultat : l'objet qui gère la connexion MySQL si tout s'est bien passé
    """
    try:
        # Création de l'objet gérant les interactions avec le serveur de BD
        engine = create_engine(f'mysql+pymysql://{user}:{passwd}@{host}/{database}')
        print("Connexion réussie")
        
        return engine

    except Exception as err:
        print("Erreur de connexion :", err)
        raise err
