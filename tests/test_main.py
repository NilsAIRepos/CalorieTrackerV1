from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_health_endpoint() -> None:
    """Health-check endpoint returns status ok."""
    resp = client.get("/api/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}
