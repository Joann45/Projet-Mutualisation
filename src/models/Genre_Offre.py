from src.app import db

# Classe Genre_Offre (table d'association)
class Genre_Offre(db.Model):
    __tablename__ = 'GENRE_OFFRE'

    id_genre = db.Column(db.Integer, db.ForeignKey('GENRE.id_genre'), primary_key=True)
    id_offre = db.Column(db.Integer, db.ForeignKey('OFFRE.id_offre'), primary_key=True)

    genre = db.relationship("Genre", back_populates="les_offres", lazy=True)
    offre = db.relationship("Offre", back_populates="les_genres", lazy=True)