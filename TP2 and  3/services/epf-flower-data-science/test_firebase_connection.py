import firebase_admin
from firebase_admin import credentials, firestore

def test_connection():
    try:
        # Initialiser Firebase
        cred = credentials.Certificate("src/config/serviceAccountKey.json")
        firebase_admin.initialize_app(cred)
        
        # Tester la connexion à Firestore
        db = firestore.client()
        
        # Essayer d'accéder à la collection parameters
        params_ref = db.collection('parameters').document('model_params')
        doc = params_ref.get()
        
        if doc.exists:
            print("✅ Connexion réussie! Document existant:", doc.to_dict())
        else:
            print("✅ Connexion réussie! Création du document...")
            params_ref.set({
                'n_estimators': 100,
                'criterion': 'gini'
            })
        
        return True
    except Exception as e:
        print("❌ Erreur de connexion:", str(e))
        return False

if __name__ == "__main__":
    test_connection() 