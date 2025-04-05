import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register():
    email = "test_user@example.com"
    password = "testpassword"

    # try register twice,
    response = client.post("/api/register", json={"email": email, "password": password})
    assert response.status_code in [200, 400]  # 200 for success，400 for existing


def test_login_success():
    email = "test_user@example.com"
    password = "testpassword"

    response = client.post("/api/login", json={"email": email, "password": password})
    assert response.status_code == 200
    assert response.json()["message"] == "Login successful"


def test_login_failure():
    response = client.post("/api/login", json={"email": "wrong@example.com", "password": "wrongpass"})
    assert response.status_code == 401
    assert response.json()["error"] == "Invalid credentials"

def test_welcome_unauthenticated():
    client.cookies.clear()
    response = client.get("/api/welcome")
    assert "Not logged in" in response.text
    assert response.status_code == 401

def test_welcome_authenticated():
    # register then login
    email = "test@example.com"
    password = "123456"

    client.post("/api/register", json={"email": email, "password": password})
    login_res = client.post("/api/login", json={"email": email, "password": password})
    assert login_res.status_code == 200

    # visit welcome with session
    response = client.get("/api/welcome")
    assert response.status_code == 200
    assert email in response.json()["email"] or email in response.text

def test_logout():
    email = "test2@example.com"
    password = "123456"

    client.post("/api/register", json={"email": email, "password": password})
    login_res = client.post("/api/login", json={"email": email, "password": password})
    assert login_res.status_code == 200

    # visit welcome
    res1 = client.get("/api/welcome")
    assert res1.status_code == 200

    # logout
    logout_res = client.post("/api/logout")
    assert logout_res.status_code == 200

    # visit welcome again
    res2 = client.get("/api/welcome")
    assert res2.status_code == 401
