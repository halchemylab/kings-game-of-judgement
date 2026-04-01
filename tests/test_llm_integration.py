# tests/test_llm_integration.py
import json
import pytest
from unittest.mock import MagicMock, patch
from llm_integration import generate_scenario_with_llm, analyze_judgment_with_llm
from models import Scenario, Analysis, WitnessResponse

@pytest.fixture
def mock_openai_client():
    with patch("llm_integration.client") as mock_client:
        yield mock_client

def test_generate_scenario_with_llm_success(mock_openai_client):
    # Mock successful JSON response
    mock_response = MagicMock()
    mock_response.choices[0].message.content = json.dumps({
        "scenario": "A dispute over a golden goose.",
        "highlighted_scenario": "A dispute over a **golden goose**.",
        "characters": ["The Farmer", "The Merchant"]
    })
    mock_openai_client.chat.completions.create.return_value = mock_response

    result = generate_scenario_with_llm("Arthur", "Simple")
    
    assert isinstance(result, Scenario)
    assert result.scenario == "A dispute over a golden goose."
    assert "The Farmer" in result.characters

def test_generate_scenario_with_llm_error(mock_openai_client):
    # Mock an API error
    mock_openai_client.chat.completions.create.side_effect = Exception("API error")
    
    result = generate_scenario_with_llm("Arthur", "Simple")
    assert "error" in result

def test_get_witness_response_with_llm_success(mock_openai_client):
    from llm_integration import get_witness_response_with_llm
    # Mock successful JSON response
    mock_response = MagicMock()
    mock_response.choices[0].message.content = json.dumps({
        "response": "I saw the merchant take the goose, Sire!"
    })
    mock_openai_client.chat.completions.create.return_value = mock_response

    result = get_witness_response_with_llm("A dispute over a golden goose.", "The Farmer", "What did you see?")
    
    assert isinstance(result, WitnessResponse)
    assert result.response == "I saw the merchant take the goose, Sire!"

def test_analyze_judgment_with_llm_success(mock_openai_client):
    # Mock successful JSON response
    mock_response = MagicMock()
    mock_response.choices[0].message.content = json.dumps({
        "thought_process": "Internal reasoning here.",
        "analysis": "You were very wise.",
        "highlighted_analysis": "You were very **wise**."
    })
    mock_openai_client.chat.completions.create.return_value = mock_response

    result = analyze_judgment_with_llm("I give the goose back.", "The golden goose case.", "Arthur")
    
    assert isinstance(result, Analysis)
    assert result.analysis == "You were very wise."
    assert result.thought_process == "Internal reasoning here."

def test_analyze_judgment_with_llm_error(mock_openai_client):
    # Mock an API error
    mock_openai_client.chat.completions.create.side_effect = Exception("API error")
    
    result = analyze_judgment_with_llm("judgment", "scenario", "Arthur")
    assert "error" in result

def test_handle_llm_response_error_dict():
    from ui.welcome import handle_llm_response
    mock_callback = MagicMock()
    
    result = handle_llm_response({"error": "Something went wrong"}, mock_callback)
    assert result is False
    mock_callback.assert_not_called()

def test_handle_llm_response_success_model():
    from ui.welcome import handle_llm_response
    mock_callback = MagicMock()
    scenario = Scenario(scenario="S", highlighted_scenario="H", characters=["C"])
    
    result = handle_llm_response(scenario, mock_callback)
    assert result is True
    mock_callback.assert_called_with(scenario)
