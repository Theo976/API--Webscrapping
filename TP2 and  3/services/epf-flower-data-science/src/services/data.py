import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
import os
from src.services.parameters import get_parameters
from pathlib import Path
import json

def process_iris_data():
    """Charge et traite les données Iris"""
    try:
        # Charger les données
        data_path = os.path.join('src', 'data', 'Iris.csv')
        iris_data = pd.read_csv(data_path)
        
        # Supprimer la colonne Id si elle existe
        if 'Id' in iris_data.columns:
            iris_data = iris_data.drop('Id', axis=1)
        
        return iris_data
    except Exception as e:
        print(f"Error processing data: {e}")
        raise e

def split_iris_data():
    """Divise les données en ensembles d'entraînement et de test"""
    data = process_iris_data()
    X = data.drop('Species', axis=1)
    y = data['Species']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Recombiner les features et les labels pour chaque ensemble
    train_data = pd.concat([X_train, y_train], axis=1)
    test_data = pd.concat([X_test, y_test], axis=1)
    
    return train_data, test_data

def train_model(train_data):
    """Entraîne le modèle avec les paramètres de Firestore"""
    try:
        # Récupérer les paramètres depuis Firestore
        parameters = get_parameters()
        if not parameters:
            parameters = {'n_estimators': 100, 'criterion': 'gini'}
        
        # Créer et entraîner le modèle
        model = RandomForestClassifier(
            n_estimators=parameters['n_estimators'],
            criterion=parameters['criterion']
        )
        
        X = train_data.drop('Species', axis=1)
        y = train_data['Species']
        model.fit(X, y)
        
        # Sauvegarder le modèle
        model_path = os.path.join('src', 'models', 'iris_model.joblib')
        joblib.dump(model, model_path)
        return model
    except Exception as e:
        print(f"Error training model: {e}")
        raise e

def load_trained_model():
    try:
        model_path = os.path.join('src', 'models', 'iris_model.joblib')
        if not os.path.exists(model_path):
            raise FileNotFoundError("Model not found")
        return joblib.load(model_path)
    except Exception as e:
        print(f"Error loading model: {e}")
        raise e

def load_model_parameters():
    params_path = Path("models/parameters.json")
    if not os.path.exists(params_path):
        raise FileNotFoundError("Parameters not found")
    with open(params_path) as f:
        return json.load(f)
