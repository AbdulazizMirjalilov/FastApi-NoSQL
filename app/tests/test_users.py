from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_register_user():
    response = client.post("/users/register/", json={
        "full_name": "John Doe",
        "email": "john@example.com",
        "password": "securepassword"
    })
    assert response.status_code == 200
    assert response.json()["message"] == "User created"
