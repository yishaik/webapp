import pytest
from unittest.mock import patch, MagicMock
from backend.api_handlers import grok_handler # Uses openai library
from backend.config import XAI_API_KEY # To check if it's mocked

@pytest.fixture(autouse=True)
def patch_grok_client():
    if grok_handler.client is not None:
        mock_client = MagicMock(spec=grok_handler.openai.OpenAI)
        mock_client.chat.completions.create = MagicMock()
        with patch.object(grok_handler, 'client', mock_client):
            yield mock_client
    else:
        mock_client_for_none_case = MagicMock(spec=grok_handler.openai.OpenAI)
        mock_client_for_none_case.chat.completions.create = MagicMock()
        with patch.object(grok_handler, 'client', mock_client_for_none_case):
            yield mock_client_for_none_case


def test_get_llm_response_success(patch_grok_client):
    if not patch_grok_client:
        pytest.skip("Grok client was None, skipping test that requires a client.")

    mock_response_content = "Test Grok response"
    mock_completion = MagicMock()
    mock_completion.choices = [MagicMock()]
    mock_completion.choices[0].message = MagicMock()
    mock_completion.choices[0].message.content = mock_response_content

    patch_grok_client.chat.completions.create.return_value = mock_completion

    prompt = "Test prompt for Grok"
    model_name = "grok-3-mini"
    response = grok_handler.get_llm_response(prompt, model_name)

    patch_grok_client.chat.completions.create.assert_called_once_with(
        model=model_name,
        messages=[{"role": "user", "content": prompt}]
    )
    assert response == mock_response_content

def test_get_llm_response_empty_prompt(patch_grok_client):
    response = grok_handler.get_llm_response("", "grok-3-mini")
    assert "Error: Prompt cannot be empty." in response
    if patch_grok_client:
        patch_grok_client.chat.completions.create.assert_not_called()

def test_get_llm_response_api_error(patch_grok_client):
    if not patch_grok_client:
        pytest.skip("Grok client was None, skipping test that requires a client.")

    patch_grok_client.chat.completions.create.side_effect = grok_handler.openai.APIConnectionError(request=MagicMock())
    prompt = "Test prompt for API error"
    model_name = "grok-3-mini"
    response = grok_handler.get_llm_response(prompt, model_name)
    assert "Error: Could not connect to xAI Grok API." in response # Error message is specific

def test_get_llm_response_authentication_error(patch_grok_client):
    if not patch_grok_client:
        pytest.skip("Grok client was None, skipping test that requires a client.")

    patch_grok_client.chat.completions.create.side_effect = grok_handler.openai.AuthenticationError(message="Auth error", response=MagicMock(), body=None)
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

def test_get_llm_response_no_choices(patch_grok_client):
    if not patch_grok_client:
        pytest.skip("Grok client was None, skipping test that requires a client.")

    mock_completion = MagicMock()
    mock_completion.choices = [] # No choices

    patch_grok_client.chat.completions.create.return_value = mock_completion

    prompt = "Test prompt for no choices"
    model_name = "grok-3-mini"
    response = grok_handler.get_llm_response(prompt, model_name)
    assert "Error: xAI Grok API returned no response or empty content." in response
