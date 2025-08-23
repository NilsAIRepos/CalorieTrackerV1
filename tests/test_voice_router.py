"""Tests for the voice WebSocket router."""

from fastapi.testclient import TestClient

from backend.main import app


def test_voice_websocket() -> None:
    """WebSocket accepts and closes immediately."""
    client = TestClient(app)
    with client.websocket_connect("/api/voice/ws"):
        pass
