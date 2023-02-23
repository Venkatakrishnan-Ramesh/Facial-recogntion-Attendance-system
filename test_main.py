from fastapi.testclient import TestClient
import main
client = TestClient(main.app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello APP"}

def test_predict_predict():
    response = client.get("/predict")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello from predict"}    