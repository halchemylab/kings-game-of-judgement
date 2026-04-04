import os
import importlib
from unittest import mock
import pytest

def test_default_model():
    """Test that the default model is gpt-5.4 when OPENAI_MODEL is not set."""
    # Patch environment without clearing it completely to preserve PATH
    with mock.patch.dict(os.environ):
        # Remove OPENAI_MODEL if it exists to test default behavior
        if "OPENAI_MODEL" in os.environ:
            del os.environ["OPENAI_MODEL"]
            
        import llm_integration
        importlib.reload(llm_integration)
        assert llm_integration.MODEL_TO_USE == "gpt-5.4"
def test_custom_model():
    """Test that the model can be configured via OPENAI_MODEL."""
    with mock.patch.dict(os.environ, {"OPENAI_MODEL": "gpt-3.5-turbo"}):
        import llm_integration
        importlib.reload(llm_integration)
        assert llm_integration.MODEL_TO_USE == "gpt-3.5-turbo"
