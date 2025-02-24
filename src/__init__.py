import src.config as config
import src.commands as commands
import src.models as models


from .app import create_app

# Créer l'application
app = create_app()