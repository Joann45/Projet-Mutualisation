from src.app import db  # Assurez-vous que `db` est importé correctement depuis votre application

# Classe Genre
class Genre(db.Model):
    __tablename__ = 'GENRE'

    id_genre = db.Column(db.Integer, primary_key=True)
    nom_genre = db.Column(db.Text)
    les_offres = db.relationship('ContenirGenre', back_populates='genre', lazy=True)