
import sys
import os
from unittest.mock import MagicMock, patch
import json
import pytest

# Add repo root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.agent import Agent, AgentResponse

# Mock Connector
class MockConnector:
    def __init__(self, responses):
        self.responses = responses
        self.call_count = 0

    def chat(self, messages):
        # Return the next response in the list
        if self.call_count < len(self.responses):
            resp = self.responses[self.call_count]
            self.call_count += 1
            return resp
        return ""

def test_agent_clarify():
    # Mock LLM to return CLARIFY action
    mock_response = json.dumps({"action": "CLARIFY", "question": "How were the eggs prepared?"})

    with patch('backend.agent.get_connector', return_value=MockConnector([mock_response])):
        agent = Agent(provider="local")
        history = [{"role": "user", "content": "I had 2 eggs"}]
        response = agent.process_message(history)

        assert response['text'] == "How were the eggs prepared?"
        assert response['draft_entry'] is None

def test_agent_search_and_calculate():
    # 1. First LLM call returns SEARCH action
    search_response = json.dumps({"action": "SEARCH", "items": ["2 boiled eggs"]})

    # 2. Second LLM call (extraction) returns nutrition data
    extraction_response = json.dumps({
        "name": "2 boiled eggs",
        "amount": "2 large",
        "calories": 156,
        "protein": 12.6,
        "carbs": 1.1,
        "fat": 10.6,
        "sugar": 1.1
    })

    # Mock search_nutrition to return some dummy text
    with patch('backend.agent.search_nutrition', return_value=["Title: Boiled Egg\nSnippet: A boiled egg has 78 calories."]):
        with patch('backend.agent.get_connector', return_value=MockConnector([search_response, extraction_response])):
            agent = Agent(provider="local")
            history = [{"role": "user", "content": "I had 2 boiled eggs"}]

            response = agent.process_message(history)

            assert "I've calculated the nutrition" in response['text']
            assert response['draft_entry'] is not None
            assert response['draft_entry']['name'] == "2 boiled eggs"
            assert response['draft_entry']['total_calories'] == 156
            assert response['draft_entry']['total_protein'] == 12.6

def test_agent_chitchat():
    mock_response = json.dumps({"action": "CHITCHAT", "reply": "Hello there!"})

    with patch('backend.agent.get_connector', return_value=MockConnector([mock_response])):
        agent = Agent(provider="local")
        history = [{"role": "user", "content": "Hi"}]
        response = agent.process_message(history)

        assert response['text'] == "Hello there!"
        assert response['draft_entry'] is None
