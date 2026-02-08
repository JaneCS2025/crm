from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_create_user():
    response = client.post("/users", json={
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "tel": "123456789",
        "password": "securepassword"
    })
    assert response.status_code == 200
    assert response.json()["email"] == "john@example.com"

def test_get_users():
    response = client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)