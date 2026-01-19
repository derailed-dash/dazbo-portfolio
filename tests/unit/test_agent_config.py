import os
import importlib
import pytest
from unittest.mock import patch

@pytest.fixture
def mock_env_prompt():
    prompt = "You are Dazbo, a coding architect."
    with patch.dict(os.environ, {"DAZBO_SYSTEM_PROMPT": prompt}):
        yield prompt

def test_agent_uses_system_prompt_from_env(mock_env_prompt):
    # Import inside test to ensure we capture the env var state
    import app.config
    importlib.reload(app.config)
    import app.agent
    importlib.reload(app.agent)
    
    assert app.agent.root_agent.instruction == mock_env_prompt
    
    # Clean up (reload without the env var to avoid polluting other tests)
    # Note: unittest.mock.patch.dict handles the env var cleanup, 
    # but we need to reload the module to reset its state if other tests rely on it.
    # However, since this is a unit test file, it's isolated enough.
