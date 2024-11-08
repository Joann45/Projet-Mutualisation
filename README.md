# StageFlow

**StageFlow** est une plateforme SaaS destinée à optimiser la mutualisation et la planification des tournées de concerts pour les organisateurs, agents, et programmateurs. Cette application permet aux réseaux fermés de festivals et de salles de concerts de collaborer efficacement et de partager des ressources pour organiser des événements.

## Équipe de développement
- **Rocma Dimba-Lau**
- **Valentin Hun**
- **Sargis Vardanyan**
- **Lenny Vergerolle**
- **Joann Raignault**

## Description

StageFlow propose un environnement collaboratif pour centraliser les efforts de planification des tournées. Les utilisateurs peuvent créer et partager des offres de concerts, consulter des propositions et collaborer avec d'autres membres des réseaux. L'application inclut la gestion des documents, des notifications par email et des outils de suivi des offres.

## Fonctionnalités principales

- **Gestion des réseaux** : Création et administration de réseaux fermés regroupant des salles et festivals.
- **Publication d'offres de concerts** : Création et partage d'offres incluant des détails sur l'artiste, le budget et les conditions techniques.
- **Réponses et validation** : Réception et validation des propositions des salles.
- **Tableau de bord** : Suivi des tournées et des propositions, gestion des documents contractuels.
- **Notifications par email** : Alertes automatiques pour les nouvelles offres et mises à jour.

## Structure du projet

```
StageFlow/
├── init.sh                 # Script d'initialisation du projet
├── README.md               # Documentation du projet
├── requirements.txt        # Liste des dépendances Python
└── src/                    # Code source de l'application
    ├── app.py              # Point d'entrée de l'application Flask
    ├── commands.py         # Commandes personnalisées pour Flask
    ├── controllers/        # Contrôleurs pour la logique métier
    │   └── ExampleController.py
    ├── forms/              # Formulaires Flask-WTF
    │   └── ExampleForm.py
    ├── __init__.py         # Initialisation du module Python
    ├── models/             # Modèles de base de données SQLAlchemy
    │   └── Example.py
    ├── templates/          # Modèles HTML pour l'interface utilisateur
    │   └── index.html
    └── views.py            # Routes et gestion des vues
```

## Installation

1. **Exécuter le script d'initialisation** :
   ```bash
   ./init.sh
   ```

   Ce script installe les dépendances et prépare l'environnement de développement.

2. **Configurer l'environnement** :
   Créez un fichier `.env` pour définir les variables nécessaires, telles que `FLASK_APP` et `FLASK_ENV`.

3. **Lancer l'application** :
   ```bash
   flask run
   ```

   Accédez à l'application sur `http://127.0.0.1:5000`.