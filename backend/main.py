"""FastAPI application wiring."""

from fastapi import FastAPI
from .routers import entries, llm

app = FastAPI(title="Calorie Tracker API")

app.include_router(entries.router, prefix="/api/entries", tags=["entries"])
app.include_router(llm.router, prefix="/api/llm", tags=["llm"])


@app.get("/")
async def root() -> dict:
    """Basic health-check endpoint."""
    return {"status": "ok"}
