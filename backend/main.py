"""FastAPI application wiring."""

from fastapi import FastAPI
from .routers import barcode, entries, image, llm, search, voice

app = FastAPI(title="Calorie Tracker API")

app.include_router(entries.router, prefix="/api/entries", tags=["entries"])
app.include_router(llm.router, prefix="/api/llm", tags=["llm"])
app.include_router(barcode.router, prefix="/api/barcode", tags=["barcode"])
app.include_router(image.router, prefix="/api/image", tags=["image"])
app.include_router(search.router, prefix="/api/search", tags=["search"])
app.include_router(voice.router, prefix="/api/voice", tags=["voice"])


@app.get("/")
async def root() -> dict:
    """Basic health-check endpoint."""
    return {"status": "ok"}
