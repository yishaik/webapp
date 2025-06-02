import pytest
from unittest.mock import patch, MagicMock
from backend.api_handlers import grok_handler # Uses openai library
from backend.config import XAI_API_KEY # To check if it's mocked

@pytest.fixture # Changed from autouse=True to be explicit in tests, or keep autouse if preferred
def mock_grok_client_fixture():
    mock_client = MagicMock(spec=grok_handler.openai.OpenAI)
    mock_client.chat = MagicMock()  # Ensure .chat is a MagicMock
    mock_client.chat.completions = MagicMock() # Ensure .chat.completions is a MagicMock
    mock_client.chat.completions.create = MagicMock() # Now .create can be set

    with patch.object(grok_handler, 'client', mock_client) as patched_client:
        yield patched_client


def test_get_llm_response_success(mock_grok_client_fixture): # Use the fixture
    mock_client = mock_grok_client_fixture
    if not mock_client: # Should always be a mock now
        pytest.skip("Grok client mock not available, skipping.")

    mock_response_content = "Test Grok response"
    mock_completion = MagicMock()
    mock_completion.choices = [MagicMock()]
    mock_completion.choices[0].message = MagicMock()
    mock_completion.choices[0].message.content = mock_response_content

    mock_client.chat.completions.create.return_value = mock_completion

    prompt = "Test prompt for Grok"
    model_name = "grok-3-mini"
    response = grok_handler.get_llm_response(prompt, model_name)

    mock_client.chat.completions.create.assert_called_once_with(
        model=model_name,
        messages=[{"role": "user", "content": prompt}]
    )
    assert response == mock_response_content

def test_get_llm_response_empty_prompt(mock_grok_client_fixture): # Use fixture
    response = grok_handler.get_llm_response("", "grok-3-mini")
    assert "Error: Prompt cannot be empty." in response
    if mock_grok_client_fixture: # mock_client from fixture
        mock_grok_client_fixture.chat.completions.create.assert_not_called()

def test_get_llm_response_api_error(mock_grok_client_fixture): # Use fixture
    mock_client = mock_grok_client_fixture
    if not mock_client:
        pytest.skip("Grok client mock not available.")

    mock_client.chat.completions.create.side_effect = grok_handler.openai.APIConnectionError(request=MagicMock())
    prompt = "Test prompt for API error"
    model_name = "grok-3-mini"
    response = grok_handler.get_llm_response(prompt, model_name)
    assert "Error: Could not connect to xAI Grok API." in response # Error message is specific

def test_get_llm_response_authentication_error(mock_grok_client_fixture): # Use fixture
    mock_client = mock_grok_client_fixture
    if not mock_client:
        pytest.skip("Grok client mock not available.")

    mock_client.chat.completions.create.side_effect = grok_handler.openai.AuthenticationError(message="Auth error", response=MagicMock(), body=None)
    prompt = "Test prompt for auth error"
    model_name = "grok-3"
    response = grok_handler.get_llm_response(prompt, model_name)
    assert "Error: xAI Grok API authentication failed." in response


@patch.object(grok_handler, 'client', None)
def test_get_llm_response_client_is_none():
    response = grok_handler.get_llm_response("Any prompt", "Any model")
    assert "xAI (Grok) client is not initialized. Check XAI_API_KEY." in response

def test_api_key_is_mocked_for_grok():
    assert XAI_API_KEY == "test_xai_key" or XAI_API_KEY is None

def test_get_llm_response_no_choices(mock_grok_client_fixture): # Use fixture
    mock_client = mock_grok_client_fixture
    if not mock_client:
        pytest.skip("Grok client mock not available.")

    mock_completion = MagicMock()
    mock_completion.choices = [] # No choices

    mock_client.chat.completions.create.return_value = mock_completion

    prompt = "Test prompt for no choices"
    model_name = "grok-3-mini"
    response = grok_handler.get_llm_response(prompt, model_name)
    assert "Error: xAI Grok API returned no response or empty content." in response
