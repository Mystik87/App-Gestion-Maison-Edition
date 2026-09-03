# App-Gestion-Maison-Edition

Backend de gestion d'une maison d'édition de livres, développé avec FastAPI,
SQLAlchemy et MySQL.

## Fonctionnalités prévues

- gestion des utilisateurs, auteurs et éditeurs ;
- suivi des manuscrits et de leurs versions ;
- gestion des livres, éditions et publications ;
- gestion des commentaires, paiements et notifications ;
- gestion des ventes et des stocks.

## Technologies

- Python 3.10 ou supérieur ;
- FastAPI ;
- SQLAlchemy ;
- MySQL avec PyMySQL ;
- Pydantic ;
- Uvicorn.

## Installation

Depuis le dossier `backend`, crée un environnement virtuel puis installe les
dépendances :

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Sous Linux ou macOS :

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Configuration de la base de données

Crée un fichier `.env` à la racine du backend :

```env
DB_HOST=localhost
DB_PORT=3307
DB_NAME=gestion_maison_edition
DB_USER=root
DB_PASSWORD=
```

Adapte les valeurs à ta configuration MySQL. Le fichier `.env` est ignoré par
Git et ne doit pas contenir de secrets partagés.

## Structure du projet

```text
backend/
├── app/
│   ├── crud.py       # opérations CRUD génériques et spécialisées
│   ├── database.py   # connexion SQLAlchemy et sessions
│   ├── main.py       # point d'entrée FastAPI
│   ├── models.py     # modèles SQLAlchemy
│   ├── schemas.py    # schémas Pydantic
│   └── routers/      # routeurs HTTP
├── requirements.txt
└── .env
```

## État actuel

Les modèles SQLAlchemy, les schémas Pydantic et les opérations CRUD de base
sont en place pour les utilisateurs et les livres. Les premiers endpoints
FastAPI sont disponibles pour ces deux ressources.

## Endpoints disponibles

| Méthode | Endpoint | Description |
| --- | --- | --- |
| GET | `/health` | Vérifier que l'API fonctionne |
| GET | `/utilisateurs` | Lister les utilisateurs |
| GET | `/utilisateurs/{id}` | Obtenir un utilisateur |
| POST | `/utilisateurs` | Créer un utilisateur |
| PUT | `/utilisateurs/{id}` | Remplacer un utilisateur |
| DELETE | `/utilisateurs/{id}` | Supprimer un utilisateur |
| GET | `/livres` | Lister les livres |
| GET | `/livres/{id}` | Obtenir un livre |
| POST | `/livres` | Créer un livre |
| PUT | `/livres/{id}` | Remplacer un livre |
| DELETE | `/livres/{id}` | Supprimer un livre |

La documentation interactive est disponible sur `/docs` lorsque le serveur
est lancé.

## Sécurité des mots de passe

Les mots de passe sont hachés avec Argon2 via `pwdlib` avant leur enregistrement
ou leur mise à jour. Ils ne sont jamais inclus dans les réponses de l'API.
Les mots de passe existants dans la base ont été contrôlés et sont déjà hachés
au format Argon2.

## Prochaines étapes

1. définir les routes pour les utilisateurs et les livres ;
2. configurer `app.main:app` ;
3. ajouter les migrations et les tests ;
4. connecter les fonctionnalités métier restantes.

## Dépôt

[App-Gestion-Maison-Edition sur GitHub](https://github.com/Mystik87/App-Gestion-Maison-Edition)
