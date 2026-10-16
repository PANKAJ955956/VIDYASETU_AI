from fastapi.testclient import TestClient
from app.main import app
from app.seed import seed

client = TestClient(app)

def test_recommendation_endpoint():
    seed()
    response = client.post("/api/recommendations/universities", json={
        "course": "B.Tech",
        "branch": "Computer Science",
        "specialization": "AI/ML",
        "location": "Delhi NCR",
        "prefer_nirf": True,
        "prefer_naac": True
    })
    assert response.status_code == 200
    assert len(response.json()) >= 1
