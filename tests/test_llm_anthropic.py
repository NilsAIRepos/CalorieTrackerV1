"""Tests for the Anthropic LLM connector."""

from backend.llm.anthropic import AnthropicConnector


def test_anthropic_chat() -> None:
    """Connector returns placeholder text."""
    conn = AnthropicConnector(client=None)
    assert conn.chat([]) == ""
