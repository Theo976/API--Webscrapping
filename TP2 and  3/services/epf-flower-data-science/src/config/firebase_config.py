import os
import firebase_admin
from firebase_admin import credentials, firestore

# Initialiser Firebase si ce n'est pas déjà fait
if not firebase_admin._apps:
    cred = credentials.Certificate("src/config/serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
    print("Firebase app initialized")

# Obtenir une référence à Firestore
db = firestore.client()
print("Firestore client created successfully")