from flask_sqlalchemy import SQLAlchemy
from src.extensions import db

from src.models.Utilisateur import Utilisateur
from src.models.Role import Role
from src.models.Notification import Notification
from src.models.Notification_Utilisateur import Notification_Utilisateur
from src.models.Offre import Offre
from src.models.Reponse import Reponse
from src.models.Utilisateur_Reseau import Utilisateur_Reseau
from src.models.Reseau import Reseau
from src.models.Document import Document
from src.models.Genre_Offre import Genre_Offre
from src.models.Genre import Genre
from src.models.Lien import Lien
from src.models.Lien_Offre import Lien_Offre
from src.models.Offre_Reseau import Offre_Reseau
from src.models.Commentaire import Commentaire