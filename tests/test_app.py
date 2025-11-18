import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_root_redirect():
    response = client.get("/")
    assert response.status_code == 200 or response.status_code == 307
    assert "/static/index.html" in str(response.url)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_for_activity_success():
    response = client.post("/activities/Chess Club/signup?email=testuser@mergington.edu")
    assert response.status_code == 200
    assert "Signed up testuser@mergington.edu for Chess Club" in response.json().get("message", "")

def test_signup_for_activity_already_signed_up():
    client.post("/activities/Programming Class/signup?email=repeat@mergington.edu")
    response = client.post("/activities/Programming Class/signup?email=repeat@mergington.edu")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"

def test_signup_for_activity_not_found():
    response = client.post("/activities/Nonexistent/signup?email=ghost@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
