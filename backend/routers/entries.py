"""Endpoints for meal entry management."""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from .. import calorie_engine, db

router = APIRouter()


class EntryIn(BaseModel):
    name: str
    nutrition: calorie_engine.Nutrition | None = None
    calories: int | None = None
    details: str | None = None
    # New fields
    protein: Optional[float] = 0.0
    carbs: Optional[float] = 0.0
    fat: Optional[float] = 0.0
    sugar: Optional[float] = 0.0


@router.post("/")
def add_entry(data: EntryIn) -> dict:
    """Store a meal entry and return its identifier and calories."""
    # If nutrition object is provided, calculate calories (legacy support)
    if data.calories is None and data.nutrition:
        cal = calorie_engine.calories(data.nutrition)
    else:
        cal = data.calories or 0

    # Use provided macros or default to 0
    prot = data.protein or 0.0
    carb = data.carbs or 0.0
    fat = data.fat or 0.0
    sugar = data.sugar or 0.0

    conn = db.get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO entries
        (name, calories, details, protein, carbs, fat, sugar)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (data.name, cal, data.details or "", prot, carb, fat, sugar),
    )
    conn.commit()
    entry_id = cur.lastrowid
    conn.close()
    return {"id": entry_id, "calories": cal}


@router.get("/")
def list_entries() -> list[dict]:
    """Return all meal entries in reverse chronological order."""
    conn = db.get_conn()
    cur = conn.cursor()
    rows = cur.execute(
        """
        SELECT id, name, calories, details, protein, carbs, fat, sugar
        FROM entries
        ORDER BY id DESC
        """
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]
