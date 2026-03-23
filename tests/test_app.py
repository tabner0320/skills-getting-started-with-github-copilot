import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_remove_participant():
    # Use a unique email for testing
    test_email = "testuser@mergington.edu"
    activity = "Chess Club"
    # Sign up
    signup_resp = client.post(f"/activities/{activity}/signup", params={"email": test_email})
    assert signup_resp.status_code == 200
    # Check participant added
    get_resp = client.get("/activities")
    assert test_email in get_resp.json()[activity]["participants"]
    # Remove participant
    remove_resp = client.delete(f"/activities/{activity}/participant", params={"email": test_email})
    assert remove_resp.status_code == 200
    # Check participant removed
    get_resp2 = client.get("/activities")
    assert test_email not in get_resp2.json()[activity]["participants"]

def test_signup_duplicate():
    activity = "Programming Class"
    email = "emma@mergington.edu"  # Already present
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert resp.status_code == 400
    assert "already signed up" in resp.json()["detail"].lower()

def test_remove_nonexistent_participant():
    activity = "Gym Class"
    email = "notfound@mergington.edu"
    resp = client.delete(f"/activities/{activity}/participant", params={"email": email})
    assert resp.status_code == 404
    assert "not found" in resp.json()["detail"].lower()
