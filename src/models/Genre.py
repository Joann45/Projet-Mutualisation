from src.app import db

# Classe Genre
class Genre(db.Model):
    __tablename__ = 'GENRE'

    id_genre = db.Column(db.Integer, primary_key=True)
    nom_genre = db.Column(db.Text)
    les_offres = db.relationship('Genre_Offre', back_populates='genre', lazy=True)