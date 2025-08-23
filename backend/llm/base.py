"""Abstractions for chat-oriented language model connectors."""

from abc import ABC, abstractmethod
from typing import Dict, List


class LLMConnector(ABC):
    """Abstract base class for chat completion models."""

    @abstractmethod
    def chat(self, messages: List[Dict[str, str]]) -> str:
        """Return response text for given chat messages."""
        raise NotImplementedError
