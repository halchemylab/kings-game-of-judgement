import pytest
from unittest.mock import MagicMock, patch
import json
from llm_integration import generate_scenario_with_llm, analyze_judgment_with_llm

@pytest.fixture
def mock_openai_client():
    with patch("llm_integration.client") as mock_client:
        yield mock_client

def test_generate_scenario_with_llm_success(mock_openai_client):
    # Mock successful JSON response
    mock_response = MagicMock()
    mock_response.choices[0].message.content = json.dumps({
        "scenario": "A dispute over a golden goose.",
        "highlighted_scenario": "A dispute over a **golden goose**."
    })
    mock_openai_client.chat.completions.create.return_value = mock_response
    
    from llm_integration import CHEAP_MODEL_TO_USE
    result = generate_scenario_with_llm("Arthur", "Simple")
    
    assert "scenario" in result
    assert "highlighted_scenario" in result
    assert "**golden goose**" in result["highlighted_scenario"]
    from unittest.mock import ANY
    mock_openai_client.chat.completions.create.assert_called_once_with(
        model=CHEAP_MODEL_TO_USE,
        messages=[
            {"role": "system", "content": "You are a master storyteller. Respond ONLY with a JSON object containing 'scenario' and 'highlighted_scenario'."},
            {"role": "user", "content": ANY}
        ],
        response_format={"type": "json_object"},
        temperature=0.8,
        max_tokens=1000
    )

def test_generate_scenario_with_llm_error(mock_openai_client):
    # Mock an API error
    mock_openai_client.chat.completions.create.side_effect = Exception("API Down")
    
    result = generate_scenario_with_llm("Arthur")
    
    assert "error" in result
    assert "API Down" in result["error"]

def test_analyze_judgment_with_llm_success(mock_openai_client):
    # Mock successful JSON response
    mock_response = MagicMock()
    mock_response.choices[0].message.content = json.dumps({
        "analysis": "You were very wise.",
        "highlighted_analysis": "You were very **wise**."
    })
    mock_openai_client.chat.completions.create.return_value = mock_response
    
    result = analyze_judgment_with_llm("I give the goose back.", "The golden goose case.", "Arthur")
    
    assert "analysis" in result
    assert "**wise**" in result["highlighted_analysis"]

def test_analyze_judgment_with_llm_no_client():
    with patch("llm_integration.client", None):
        result = analyze_judgment_with_llm("j", "s", "p")
        assert "error" in result
        assert "not configured" in result["error"]

def test_prompt_difficulty_constraints():
    from llm_integration import SCENARIO_GENERATION_JSON_PROMPT_TEMPLATE
    assert "Strictly follow these structural constraints" in SCENARIO_GENERATION_JSON_PROMPT_TEMPLATE
    assert "**Simple**: Focus on exactly two parties" in SCENARIO_GENERATION_JSON_PROMPT_TEMPLATE
    assert "**Moderate**: Introduce a third party" in SCENARIO_GENERATION_JSON_PROMPT_TEMPLATE
    assert "**Complex**: Involve systemic societal issues" in SCENARIO_GENERATION_JSON_PROMPT_TEMPLATE
