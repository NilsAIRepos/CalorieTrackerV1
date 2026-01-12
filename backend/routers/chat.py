"""Endpoints for the chat agent."""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional, Any
import logging

from ..agent import Agent
from .. import db

router = APIRouter()

# Instantiate the agent globally or per request
# For this V1, we use a global instance which might be configured via env vars
# We default to 'local' to avoid startup crash if no keys are present
agent = Agent(provider="local")

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    provider: Optional[str] = None # Default to None, let backend logic decide
    model: Optional[str] = None

class Ingredient(BaseModel):
    name: str
    amount: str
    calories: int
    protein: float
    carbs: float
    fat: float
    sugar: float

class MealPlan(BaseModel):
    name: str
    ingredients: List[Ingredient]
    total_calories: int
    total_protein: float
    total_carbs: float
    total_fat: float
    total_sugar: float

class ChatResponse(BaseModel):
    text: str
    draft_entry: Optional[MealPlan] = None

@router.post("/message", response_model=ChatResponse)
def chat_message(req: ChatRequest):
    """
    Process a user message through the Agent pipeline.
    """
    # 1. Log User Message
    last_msg = req.messages[-1]
    log_id = None
    if last_msg.role == 'user':
        log_id = log_user_message(last_msg.content)

    # 2. Re-configure agent if provider changed
    # (In a real app, we might pool agents or pass config to process_message)
    # Here we just create a new one for simplicity if needed, or use the global one.
    # To support the `provider` param:
    provider_to_use = req.provider or "local"
    try:
        current_agent = Agent(provider=provider_to_use, model=req.model)
    except Exception:
        # Fallback to local if provider init fails (e.g. missing keys)
        current_agent = Agent(provider="local")

    # 3. Process
    # Convert Pydantic models to dicts
    history_dicts = [m.model_dump() for m in req.messages]
    response_data = current_agent.process_message(history_dicts)

    # 4. Log Bot Response (Update the specific row if we created one, else new row)
    log_bot_response(log_id, response_data['text'])

    return response_data

def log_user_message(msg: str) -> Optional[int]:
    """Log user message and return the row ID."""
    try:
        conn = db.get_conn()
        cur = conn.cursor()
        cur.execute("INSERT INTO chat_logs (user_message) VALUES (?)", (msg,))
        row_id = cur.lastrowid
        conn.commit()
        conn.close()
        return row_id
    except Exception as e:
        print(f"Logging error (User): {e}")
        return None

def log_bot_response(row_id: Optional[int], msg: str):
    """Log bot response, updating the row if ID is provided."""
    try:
        conn = db.get_conn()
        cur = conn.cursor()
        if row_id:
            cur.execute("UPDATE chat_logs SET bot_response = ? WHERE id = ?", (msg, row_id))
        else:
            cur.execute("INSERT INTO chat_logs (bot_response) VALUES (?)", (msg,))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Logging error (Bot): {e}")
