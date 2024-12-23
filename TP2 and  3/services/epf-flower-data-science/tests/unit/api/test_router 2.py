import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_process_data():
    response = client.get("/data/process")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_split_data():
    response = client.get("/data/split")
    assert response.status_code == 200
    assert "train" in response.json()
    assert "test" in response.json()

def test_train():
    response = client.get("/train")
    assert response.status_code == 200
    assert response.json() == {"status": "Model trained successfully"}

def test_predict():
    response = client.get("/predict", params={
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2
    })
    assert response.status_code == 200
    assert "prediction" in response.json() 

def test_get_datasets():
    response = client.get("/config/datasets")
    assert response.status_code == 200
    assert "datasets" in response.json()

def test_add_dataset():
    new_dataset = {
        "name": "test_dataset",
        "url": "https://test.url/dataset"
    }
    response = client.post("/config/datasets", json=new_dataset)
    assert response.status_code == 200
    assert response.json()["message"] == "Dataset added successfully"

def test_update_dataset():
    updated_dataset = {
        "name": "iris",
        "url": "https://new.url/dataset"
    }
    response = client.put("/config/datasets/iris", json=updated_dataset)
    assert response.status_code == 200
    assert response.json()["message"] == "Dataset updated successfully"

def test_dataset_not_found():
    response = client.put("/config/datasets/nonexistent", 
                         json={"name": "test", "url": "test"})
    assert response.status_code == 404 

def test_model_parameters_loading():
    from src.services.data import load_model_parameters
    
    # Test si les paramètres sont chargés correctement
    params = load_model_parameters()
    assert "model_name" in params
    assert params["model_name"] == "RandomForestClassifier"
    assert "parameters" in params
    assert "n_estimators" in params["parameters"]
    assert "criterion" in params["parameters"]

def test_model_training_with_parameters():
    from src.services.data import train_model, split_iris_data
    
    # Test si le modèle s'entraîne avec les paramètres
    train, _ = split_iris_data()
    model = train_model(train)
    
    # Vérifier que le modèle a les bons paramètres
    assert model.n_estimators == 100
    assert model.criterion == "gini"