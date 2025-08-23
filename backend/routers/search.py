"""Food database search endpoints."""

from fastapi import APIRouter, Query

router = APIRouter()


@router.get("/")
async def search_food(q: str = Query(...)) -> list[dict]:
    """Search the food database.

    Placeholder implementation returning an empty list.
    """
    return []
