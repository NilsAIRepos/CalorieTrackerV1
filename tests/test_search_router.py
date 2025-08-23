"""Tests for the search router."""

from fastapi.testclient import TestClient

from backend.main import app


def test_food_search() -> None:
    """Food search returns an empty list placeholder."""
    client = TestClient(app)
    res = client.get("/api/search/", params={"q": "apple"})
    assert res.status_code == 200
    assert res.json() == []
