from src.app import db

# Classe Document
class Document(db.Model):
    __tablename__ = 'DOCUMENT'

    id_doc = db.Column(db.Integer, primary_key=True)
    nom_doc = db.Column(db.Text)
    details_doc = db.Column(db.Text)
    id_offre = db.Column(db.Integer, db.ForeignKey('OFFRE.id_offre'))
    offre = db.relationship('Offre', back_populates='les_documents', lazy=True)