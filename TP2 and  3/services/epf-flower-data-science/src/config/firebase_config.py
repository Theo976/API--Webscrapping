import os
import firebase_admin
from firebase_admin import credentials, firestore

def get_firebase_app():
    """Initialize Firebase app with error handling"""
    try:
        if not firebase_admin._apps:
            cred = credentials.Certificate("src/config/serviceAccountKey.json")
            firebase_admin.initialize_app(cred)
            print("Firebase app initialized")
        return firebase_admin.get_app()
    except ValueError as e:
        print(f"Warning: Firebase initialization failed: {e}")
        return None

# Initialize Firebase app
app = get_firebase_app()

# Get Firestore client
try:
    db = firestore.client()
except Exception as e:
    print(f"Warning: Firestore client creation failed: {e}")
    db = None

# Initialiser la collection parameters si elle n'existe pas
def init_parameters():
    """Step 13: Crée la collection parameters avec les valeurs par défaut"""
    try:
        params_ref = db.collection('parameters').document('model_params')
        if not params_ref.get().exists:
            default_params = {
                'n_estimators': 100,
                'criterion': 'gini'
            }
            params_ref.set(default_params)
            print("Parameters collection initialized")
        return True
    except Exception as e:
        print(f"Error initializing parameters: {e}")
        return False

# Initialiser les paramètres au démarrage
init_parameters()