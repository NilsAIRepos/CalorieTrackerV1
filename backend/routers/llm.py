from fastapi import APIRouter
from pydantic import BaseModel

from ..llm import OpenAIConnector, LocalConnector, LLMConnector, OllamaConnector

router = APIRouter()


def get_connector(provider: str = "local", base_url: str | None = None, model: str | None = None) -> LLMConnector:
    if provider == "openai":
        try:
            import openai
        except Exception:  # pragma: no cover - optional dependency
            raise RuntimeError("openai package not installed")
        client = openai.OpenAI()
        return OpenAIConnector(client)
    if provider == "ollama":
        return OllamaConnector(base_url or "http://localhost:11434", model or "llama3.2:latest")
    return LocalConnector()


class ChatRequest(BaseModel):
    messages: list[dict]


@router.post("/chat")
def chat(req: ChatRequest, provider: str = "local", base_url: str | None = None, model: str | None = None) -> dict:
    connector = get_connector(provider, base_url, model)
    reply = connector.chat(req.messages)
    return {"reply": reply}
