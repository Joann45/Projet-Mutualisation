from src.app import db  # Assurez-vous que `db` est importé correctement depuis votre application

# Classe PlageDate
class PlageDate(db.Model):
    __tablename__ = 'PLAGE_DATE'

    id_plage = db.Column(db.Integer, primary_key=True)
    date_deb = db.Column(db.Date)
    date_fin = db.Column(db.Date)
    les_offres = db.relationship('Offre', back_populates='date', lazy=True)