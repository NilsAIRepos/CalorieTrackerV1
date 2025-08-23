"""Connector for local Ollama servers."""

from typing import Dict, List

import requests

from .base import LLMConnector


class OllamaConnector(LLMConnector):
    """Interact with an Ollama instance via its REST API."""

    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3.2:latest"):
        self.base_url = base_url.rstrip('/')
        self.model = model

    def chat(self, messages: List[Dict[str, str]]) -> str:
        payload = {"model": self.model, "messages": messages}
        resp = requests.post(f"{self.base_url}/v1/chat/completions", json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"].strip()
