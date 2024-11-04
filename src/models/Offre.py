from src.app import db  # Assurez-vous que `db` est importé correctement depuis votre application

# Classe Offre
class Offre(db.Model):
    __tablename__ = 'OFFRE'

    id_offre = db.Column(db.Integer, primary_key=True)
    nom_offre = db.Column(db.Text)
    description = db.Column(db.Text)
    date_limite = db.Column(db.Date)
    budget = db.Column(db.Numeric)
    capacite_min = db.Column(db.Integer)
    capacite_max = db.Column(db.Integer)
    etat = db.Column(db.Text)

    id_orga = db.Column(db.Integer, db.ForeignKey('ORGANISATEUR.id_orga'))
    id_loc = db.Column(db.Integer, db.ForeignKey('LOCALISATION.id_loc'))
    id_plage = db.Column(db.Integer, db.ForeignKey('PLAGE_DATE.id_plage'))

    # Relations
    orga = db.relationship('Organisateur', backref=db.backref('les_offres', lazy=True))
    loc = db.relationship('Localisation', backref=db.backref('les_offres', lazy=True))
    date = db.relationship('PlageDate', backref=db.backref('les_offres', lazy=True))
    les_documents = db.relationship('Document', back_populates='offre', lazy=True)
    les_genres = db.relationship('ContenirGenre', back_populates='offre', lazy=True)
    les_liens = db.relationship('ContenirLien', back_populates='offre', lazy=True)
    les_reponses_orgas = db.relationship('Repondre', back_populates='offre_orga', lazy=True)
    les_reseaux = db.relationship('PartagerOffre', back_populates='offre', lazy=True)