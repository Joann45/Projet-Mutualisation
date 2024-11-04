import click
from .app import app, db

@app.cli.command()
@click.argument('filename')
def loaddb(filename):
    '''Creates the tables and populates them with data.'''
    # Création de toutes les tables
    db.create_all()
    
    # Import des modèles
    import models.models as md
    import yaml
    with open(filename, 'r') as file:
        data = yaml.safe_load(file)

    Organisateurs = {}
    for orga in 
    
    # Première passe: création de tous les auteurs
    authors = {}
    for b in books:
        a = b["author"]
        if a not in authors:
            o = Author(name=a)
            db.session.add(o)
            authors[a] = o
    db.session.commit()
    
    # Deuxième passe: création de tous les livres
    for b in books:
        a = authors[b["author"]]
        o = Book(
            price=b["price"],
            title=b["title"],
            url=b["url"],
            img=b["img"],
            author_id=a.id
        )
        db.session.add(o)
    db.session.commit()