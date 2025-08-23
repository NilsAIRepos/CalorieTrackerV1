from abc import ABC, abstractmethod
from typing import List, Dict


class LLMConnector(ABC):
    """Abstract base class for chat completion models."""

    @abstractmethod
    def chat(self, messages: List[Dict[str, str]]) -> str:
        """Return response text for given chat messages."""
        raise NotImplementedError
