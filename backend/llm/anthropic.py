"""Connector for Anthropic's Claude models."""

from typing import Dict, List

from .base import LLMConnector


class AnthropicConnector(LLMConnector):
    """Interact with Anthropic's chat completion API."""

    def __init__(self, client):
        self.client = client

    def chat(self, messages: List[Dict[str, str]]) -> str:
        """Return a response from the Anthropic client.

        Placeholder implementation that returns an empty string.
        """
        return ""
