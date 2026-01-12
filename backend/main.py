"""FastAPI application wiring."""

from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .routers import entries, llm, chat

app = FastAPI(title="Calorie Tracker API")

app.include_router(entries.router, prefix="/api/entries", tags=["entries"])
app.include_router(llm.router, prefix="/api/llm", tags=["llm"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])


@app.get("/api/health")
async def health() -> dict:
    """Basic health-check endpoint."""
    return {"status": "ok"}


frontend_dir = Path(__file__).resolve().parent.parent / "frontend"
app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")
