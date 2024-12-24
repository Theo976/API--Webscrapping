from firebase_admin import credentials, firestore, initialize_app

def init_firestore():
    """Initialise Firestore avec les paramètres par défaut"""
    db = firestore.client()
    
    # Créer la collection parameters si elle n'existe pas
    params_ref = db.collection('parameters').document('model_params')
    if not params_ref.get().exists:
        params_ref.set({
            'n_estimators': 100,
            'criterion': 'gini'
        })
    
    return db 