# EPF Flower Data Science API

API de classification des fleurs d'Iris utilisant FastAPI et Firebase.

![Tests](https://github.com/Theo976/API---Webscrapping/actions/workflows/python-app.yml/badge.svg)

## Fonctionnalités

- 🌸 Prédiction de variétés d'Iris
- 🔐 Authentification avec Firebase
- 💾 Stockage des paramètres dans Firestore
- 🛡️ Protection contre les attaques DoS
- ✅ Tests automatisés

## Installation
Installer les dépendances
```bash
pip install -r requirements.txt
```


## Configuration

1. **Firebase** :
   - Créer un projet sur [Firebase Console](https://console.firebase.google.com/)
   - Télécharger `serviceAccountKey.json`
   - Le placer dans `src/config/`

2. **Environnement** :
   ```bash
   # Créer un environnement virtuel
   python -m venv venv
   source venv/bin/activate  # ou venv\Scripts\activate sous Windows
   ```

## Utilisation

1. **Lancer l'API** :
   ```bash
   uvicorn main:app --reload
   ```

2. **Documentation** :
   - Swagger UI : http://localhost:8000/docs
   - ReDoc : http://localhost:8000/redoc

## Tests
Lancer tous les tests
```bash
pytest tests/ -v
```
Lancer des tests spécifiques
```bash
pytest tests/test_model.py -v
```

epf-flower-data-science/
├── src/
│ ├── api/ # Routes API
│ ├── auth/ # Authentification
│ ├── config/ # Configuration
│ ├── models/ # Modèles ML
│ └── services/ # Services
├── tests/ # Tests
└── main.py # Point d'entrée

## CI/CD

- GitHub Actions pour les tests automatiques
- Badge de statut des tests
- Déploiement automatique (à venir)

## Auteur

Théo Vassal

## Licence

MIT