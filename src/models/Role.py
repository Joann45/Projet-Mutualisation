from src.extensions import db
from flask_security import RoleMixin, current_user
from functools import wraps
from flask import abort

class Role(db.Model, RoleMixin):
    __tablename__ = 'ROLE'
    id_role = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    users = db.relationship('Utilisateur', backref='role')
    
def roles(*roles):
    """Vérifie si l'utilisateur a un rôle parmi ceux passés en paramètre
    
    Args:
        *roles : Les rôles à vérifier
        
    Returns:
        decorator : La fonction décorée
    Examples:
        >>> @roles("Administrateur","Organisateur")
        >>> def home():
        >>>     return render_template('home.html')
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not Role.query.get(current_user.role_id).name in roles:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator