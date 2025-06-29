import pytest
from fastapi.testclient import TestClient
from main import app
from database import Base, engine

client = TestClient(app)

@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_content_scheduling(test_db):
    # Test scheduling a post
    response = client.post("/api/content", json={
        "account_id": 1,
        "content": "Test post",
        "scheduled_time": "2025-07-01T12:00:00"
    })
    assert response.status_code == 200
    assert response.json()["content"] == "Test post"

def test_engagement_tracking(test_db):
    # Test getting engagement metrics
    response = client.get("/api/engagement/account/1/summary")
    assert response.status_code == 200
    assert "total_likes" in response.json()

def test_hashtag_optimization(test_db):
    # Test getting hashtag suggestions
    response = client.post("/api/hashtags/suggestions", json={
        "content": "This is a test post",
        "limit": 5
    })
    assert response.status_code == 200
    assert len(response.json()) <= 5

def test_platform_integration(test_db):
    # Test connecting a platform
    response = client.post("/api/platforms/connect", json={
        "platform": "twitter",
        "auth_data": {"token": "test_token"}
    })
    assert response.status_code == 200
    assert response.json()["platform"] == "twitter"