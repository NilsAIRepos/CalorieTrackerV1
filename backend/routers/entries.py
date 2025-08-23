from fastapi import APIRouter
from pydantic import BaseModel

from .. import calorie_engine, db

router = APIRouter()


class EntryIn(BaseModel):
    name: str
    nutrition: calorie_engine.Nutrition | None = None
    calories: int | None = None
    details: str | None = None


@router.post("/")
def add_entry(data: EntryIn) -> dict:
    if data.calories is None and data.nutrition:
        cal = calorie_engine.calories(data.nutrition)
    else:
        cal = data.calories or 0
    conn = db.get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO entries (name, calories, details) VALUES (?, ?, ?)",
        (data.name, cal, data.details or ""),
    )
    conn.commit()
    entry_id = cur.lastrowid
    conn.close()
    return {"id": entry_id, "calories": cal}


@router.get("/")
def list_entries() -> list[dict]:
    conn = db.get_conn()
    cur = conn.cursor()
    rows = cur.execute(
        "SELECT id, name, calories, details FROM entries ORDER BY id DESC"
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]
