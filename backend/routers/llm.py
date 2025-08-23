"""Endpoints for interacting with language models."""

from fastapi import APIRouter
from pydantic import BaseModel

from ..llm.base import LLMConnector
from ..llm.local import LocalConnector

router = APIRouter()


def get_connector(
    provider: str = "local", base_url: str | None = None, model: str | None = None
) -> LLMConnector:
    """Return an LLM connector for the requested provider."""
    if provider == "openai":
        try:
            import openai
            from ..llm.openai import OpenAIConnector
        except Exception:  # pragma: no cover - optional dependency
            raise RuntimeError("openai package not installed")
        client = openai.OpenAI()
        return OpenAIConnector(client)
    if provider == "anthropic":
        try:
            import anthropic
            from ..llm.anthropic import AnthropicConnector
        except Exception:  # pragma: no cover - optional dependency
            raise RuntimeError("anthropic package not installed")
        client = anthropic.Anthropic()
        return AnthropicConnector(client)
    if provider == "ollama":
        from ..llm.ollama import OllamaConnector

        return OllamaConnector(base_url or "http://localhost:11434", model or "llama3.2:latest")
    return LocalConnector()


class ChatRequest(BaseModel):
    messages: list[dict]


@router.post("/chat")
def chat(
    req: ChatRequest,
    provider: str = "local",
    base_url: str | None = None,
    model: str | None = None,
) -> dict:
    """Proxy chat messages to the selected LLM provider."""
    connector = get_connector(provider, base_url, model)
    reply = connector.chat(req.messages)
    return {"reply": reply}
