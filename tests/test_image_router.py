"""Tests for the image router."""

from fastapi.testclient import TestClient

from backend.main import app


def test_image_upload() -> None:
    """Image upload returns the filename."""
    client = TestClient(app)
    files = {"file": ("meal.jpg", b"data", "image/jpeg")}
    res = client.post("/api/image/", files=files)
    assert res.status_code == 200
    assert res.json() == {"filename": "meal.jpg"}
