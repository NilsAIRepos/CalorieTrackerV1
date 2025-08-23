"""WebSocket endpoint for voice input."""

from fastapi import APIRouter, WebSocket

router = APIRouter()


@router.websocket("/ws")
async def voice_stream(ws: WebSocket) -> None:
    """Handle a voice stream connection.

    Placeholder implementation that immediately closes the socket.
    """
    await ws.accept()
    await ws.close()
