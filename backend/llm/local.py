"""Local dummy model connector."""

from typing import Dict, List

from .base import LLMConnector


class LocalConnector(LLMConnector):
    """Dummy local model connector for offline inference."""

    def chat(self, messages: List[Dict[str, str]]) -> str:  # pragma: no cover - placeholder
        prompt = messages[-1]["content"] if messages else ""
        return f"Local model response to: {prompt}"
