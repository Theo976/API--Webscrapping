from src.config.firebase_config import db

def get_parameters():
    """Récupère les paramètres depuis Firestore"""
    try:
        doc_ref = db.collection('parameters').document('model_params')
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        # Si le document n'existe pas, retourner les valeurs par défaut
        default_params = {"n_estimators": 100, "criterion": "gini"}
        # Créer le document avec les valeurs par défaut
        doc_ref.set(default_params)
        return default_params
    except Exception as e:
        print(f"Error getting parameters: {e}")
        # En cas d'erreur, retourner les valeurs par défaut
        return {"n_estimators": 100, "criterion": "gini"}

def update_parameters(params):
    """Met à jour les paramètres dans Firestore"""
    try:
        doc_ref = db.collection('parameters').document('model_params')
        doc_ref.set(params)
        return params
    except Exception as e:
        print(f"Error updating parameters: {e}")
        raise e
