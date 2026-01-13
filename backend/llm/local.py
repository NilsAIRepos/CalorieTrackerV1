"""Local dummy model connector."""

from typing import Dict, List

from .base import LLMConnector


class LocalConnector(LLMConnector):
    """Dummy local model connector for offline inference."""

    def chat(self, messages: List[Dict[str, str]]) -> str:  # pragma: no cover - placeholder
        # Return a valid JSON response so the Agent doesn't crash if this fallback is used.
        # We'll just say we can't help much.
        return '{"action": "CHITCHAT", "reply": "I am a dummy local model. Please configure a real LLM provider (OpenAI or Ollama) to log meals."}'
