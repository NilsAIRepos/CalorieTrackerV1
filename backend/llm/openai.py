from typing import List, Dict

from .base import LLMConnector


class OpenAIConnector(LLMConnector):
    """Connector for OpenAI's chat API."""

    def __init__(self, client):
        self.client = client

    def chat(self, messages: List[Dict[str, str]]) -> str:
        """Call OpenAI client to get a response."""
        response = self.client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
        return response.choices[0].message.content.strip()
