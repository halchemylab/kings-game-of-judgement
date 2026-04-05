import json
import pytest
from unittest.mock import MagicMock, patch
from llm_integration import get_witness_response_with_llm
from models import WitnessResponse, InquiryEntry

@pytest.fixture
def mock_openai_client():
    with patch("llm_integration.client") as mock_client:
        yield mock_client

def test_get_witness_response_with_history(mock_openai_client):
    # Mock successful JSON response
    mock_response = MagicMock()
    mock_response.choices[0].message.content = json.dumps({
        "response": "As I said before, I was at the market."
    })
    mock_openai_client.chat.completions.create.return_value = mock_response

    scenario = "A merchant is accused of theft."
    character = "The Merchant"
    question = "Are you sure you were at the market?"
    history = [
        InquiryEntry(character="The Merchant", question="Where were you?", response="I was at the market.")
    ]

    result = get_witness_response_with_llm(scenario, character, question, history=history)
    
    assert isinstance(result, WitnessResponse)
    assert result.response == "As I said before, I was at the market."
    
    # Check if history was included in the prompt
    args, kwargs = mock_openai_client.chat.completions.create.call_args
    prompt = kwargs['messages'][1]['content']
    assert "Previous Conversation History with this Character:" in prompt
    assert "The King asked: Where were you?" in prompt
    assert "Your previous response: I was at the market." in prompt

def test_get_witness_response_filters_history(mock_openai_client):
    # Mock successful JSON response
    mock_response = MagicMock()
    mock_response.choices[0].message.content = json.dumps({
        "response": "I know nothing of the merchant's business."
    })
    mock_openai_client.chat.completions.create.return_value = mock_response

    scenario = "A merchant is accused of theft."
    character = "The Guard"
    question = "What do you know?"
    history = [
        InquiryEntry(character="The Merchant", question="Where were you?", response="I was at the market.")
    ]

    result = get_witness_response_with_llm(scenario, character, question, history=history)
    
    # Check if history for DIFFERENT character was EXCLUDED from the prompt
    args, kwargs = mock_openai_client.chat.completions.create.call_args
    prompt = kwargs['messages'][1]['content']
    assert "Previous Conversation History with this Character:" not in prompt
    assert "The Merchant" not in prompt
