import src.config as config
import src.models as models
from .app import create_app
from flask_mail import Mail, Message
# Créer l'application
app = create_app()

import src.commands as commands