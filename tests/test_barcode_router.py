"""Tests for the barcode router."""

from fastapi.testclient import TestClient

from backend.main import app


def test_barcode_lookup() -> None:
    """Barcode lookup echoes the code."""
    client = TestClient(app)
    res = client.get("/api/barcode/123")
    assert res.status_code == 200
    assert res.json() == {"code": "123", "name": "unknown"}
