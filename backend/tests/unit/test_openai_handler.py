import pytest
from unittest.mock import patch, MagicMock
from backend.api_handlers import openai_handler
from backend.config import OPENAI_API_KEY # To check if it's mocked

# This ensures that the client is patched for all tests in this module
@pytest.fixture(autouse=True)
def patch_openai_client():
    # Only proceed with patching if the original client was potentially initialized
    if openai_handler.client is not None:
        mock_client = MagicMock(spec=openai_handler.openai.OpenAI)
        # Mock the chat.completions.create method
        mock_client.chat.completions.create = MagicMock()
        with patch.object(openai_handler, 'client', mock_client):
            yield mock_client
    else:
        # If client is None (e.g. API key was missing during initial load),
        # we can't patch its methods directly.
        # Tests for this scenario (client is None) should be handled separately
        # or by ensuring the fixture provides a mock client regardless.
        # For simplicity, if client is None, we yield None, and tests should check for this.
        # Alternatively, force a MagicMock for 'client' even if it was None.
        # This allows testing the get_llm_response logic assuming a client object exists.
        # The actual "client is None" case is tested below.
        mock_client_for_none_case = MagicMock(spec=openai_handler.openai.OpenAI)
        mock_client_for_none_case.chat.completions.create = MagicMock()
        with patch.object(openai_handler, 'client', mock_client_for_none_case):
             yield mock_client_for_none_case


def test_get_llm_response_success(patch_openai_client):
    if not patch_openai_client: # Skip if client was None and not forcibly mocked by fixture
        pytest.skip("OpenAI client was None, skipping test that requires a client.")

    mock_response_content = "Test OpenAI response"
    # Configure the mock completion object structure
    mock_completion = MagicMock()
    mock_completion.choices = [MagicMock()]
    mock_completion.choices[0].message = MagicMock()
    mock_completion.choices[0].message.content = mock_response_content

    patch_openai_client.chat.completions.create.return_value = mock_completion

    prompt = "Test prompt"
    model_name = "gpt-4o"
    response = openai_handler.get_llm_response(prompt, model_name)

    patch_openai_client.chat.completions.create.assert_called_once_with(
        model=model_name,
        messages=[{"role": "user", "content": prompt}]
    )
    assert response == mock_response_content

def test_get_llm_response_empty_prompt(patch_openai_client):
    response = openai_handler.get_llm_response("", "gpt-4o")
    assert "Error: Prompt cannot be empty." in response
    if patch_openai_client: # client should not be called if prompt is empty
        patch_openai_client.chat.completions.create.assert_not_called()


def test_get_llm_response_api_error(patch_openai_client):
    if not patch_openai_client:
        pytest.skip("OpenAI client was None, skipping test that requires a client.")

    # Simulate an API error
    patch_openai_client.chat.completions.create.side_effect = openai_handler.openai.APIConnectionError(request=MagicMock())

    prompt = "Test prompt for API error"
    model_name = "gpt-4o"
    response = openai_handler.get_llm_response(prompt, model_name)

    assert "Error: Could not connect to OpenAI API." in response

def test_get_llm_response_rate_limit_error(patch_openai_client):
    if not patch_openai_client:
        pytest.skip("OpenAI client was None, skipping test that requires a client.")

    patch_openai_client.chat.completions.create.side_effect = openai_handler.openai.RateLimitError(message="Rate limit exceeded", response=MagicMock(), body=None)
    prompt = "Test prompt for rate limit"
    model_name = "gpt-4o"
    response = openai_handler.get_llm_response(prompt, model_name)
    assert "Error: OpenAI API rate limit exceeded." in response

def test_get_llm_response_authentication_error(patch_openai_client):
    if not patch_openai_client:
        pytest.skip("OpenAI client was None, skipping test that requires a client.")

    patch_openai_client.chat.completions.create.side_effect = openai_handler.openai.AuthenticationError(message="Auth error", response=MagicMock(), body=None)
    prompt = "Test prompt for auth error"
    model_name = "gpt-4o"
    response = openai_handler.get_llm_response(prompt, model_name)
    assert "Error: OpenAI API authentication failed." in response

def test_get_llm_response_generic_exception(patch_openai_client):
    if not patch_openai_client:
        pytest.skip("OpenAI client was None, skipping test that requires a client.")

    patch_openai_client.chat.completions.create.side_effect = Exception("Some generic error")
    prompt = "Test prompt for generic error"
    model_name = "gpt-4o"
    response = openai_handler.get_llm_response(prompt, model_name)
    assert "Error: An unexpected error occurred while contacting OpenAI." in response

@patch.object(openai_handler, 'client', None) # Test case where client is None (e.g. API key missing)
def test_get_llm_response_client_is_none():
    # This test specifically checks the scenario where the client was not initialized.
    # The autouse fixture might re-patch 'client', so we patch it directly to None here.
    response = openai_handler.get_llm_response("Any prompt", "Any model")
    assert "OpenAI client is not initialized. Check API key." in response

def test_api_key_is_mocked_for_openai():
    # Check that the API key used by the config module (if re-imported or accessed) is the mocked one.
    # This relies on the conftest.py session-scoped autouse fixture.
    assert OPENAI_API_KEY == "test_openai_key" or OPENAI_API_KEY is None
    # Or, if openai_handler.client was initialized with a key, check that one:
    # if openai_handler.client:
    #     assert openai_handler.client.api_key == "test_openai_key"

def test_get_llm_response_no_choices(patch_openai_client):
    if not patch_openai_client:
        pytest.skip("OpenAI client was None, skipping test that requires a client.")

    mock_completion = MagicMock()
    mock_completion.choices = [] # No choices

    patch_openai_client.chat.completions.create.return_value = mock_completion

    prompt = "Test prompt for no choices"
    model_name = "gpt-4o"
    response = openai_handler.get_llm_response(prompt, model_name)
    assert "Error: OpenAI API returned no response or empty content." in response

def test_get_llm_response_empty_content(patch_openai_client):
    if not patch_openai_client:
        pytest.skip("OpenAI client was None, skipping test that requires a client.")

    mock_completion = MagicMock()
    mock_completion.choices = [MagicMock()]
    mock_completion.choices[0].message = MagicMock()
    mock_completion.choices[0].message.content = None # Empty content

    patch_openai_client.chat.completions.create.return_value = mock_completion

    prompt = "Test prompt for empty content"
    model_name = "gpt-4o"
    response = openai_handler.get_llm_response(prompt, model_name)
    assert response == "" # Handler should return empty string for None content

    mock_completion.choices[0].message.content = "  " # Whitespace content
    patch_openai_client.chat.completions.create.return_value = mock_completion
    response_ws = openai_handler.get_llm_response(prompt, model_name)
    assert response_ws == "" # Handler should strip whitespace and return empty string

    mock_completion.choices[0].message.content = "" # Empty string content
    patch_openai_client.chat.completions.create.return_value = mock_completion
    response_empty_str = openai_handler.get_llm_response(prompt, model_name)
    assert response_empty_str == "" # Handler should return empty string for empty string content
