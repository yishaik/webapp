import pytest
from unittest.mock import patch, MagicMock
from backend.api_handlers import claude_handler
from backend.config import ANTHROPIC_API_KEY # To check if it's mocked

@pytest.fixture
def mock_anthropic_client_fixture(): # Renamed to avoid autouse if not always desired, or keep autouse if it's fine
    mock_client = MagicMock(spec=claude_handler.anthropic.Anthropic)
    mock_client.messages = MagicMock()  # Ensure .messages is a MagicMock
    mock_client.messages.create = MagicMock() # Now .create can be set on .messages

    with patch.object(claude_handler, 'client', mock_client) as patched_client:
        yield patched_client

def test_get_llm_response_success(mock_anthropic_client_fixture): # Use the fixture
    # patch_anthropic_client is now mock_anthropic_client_fixture
    mock_client = mock_anthropic_client_fixture
    if not mock_client: # Should always be a mock now due to fixture structure
        pytest.skip("Anthropic client mock not available, skipping.")

    mock_response_text = "Test Anthropic response"
    mock_api_response = MagicMock()
    # Simulate the structure of Anthropic's response: list of content blocks
    mock_text_block = MagicMock()
    mock_text_block.type = "text"
    mock_text_block.text = mock_response_text
    mock_api_response.content = [mock_text_block]

    mock_client.messages.create.return_value = mock_api_response

    prompt = "Test prompt for Claude"
    model_name = "claude-3-opus-20240229"
    response = claude_handler.get_llm_response(prompt, model_name)

    mock_client.messages.create.assert_called_once_with(
        model=model_name,
        max_tokens=4096, # As per handler default
        messages=[{"role": "user", "content": prompt}]
    )
    assert response == mock_response_text

def test_get_llm_response_empty_prompt(mock_anthropic_client_fixture): # Use fixture
    response = claude_handler.get_llm_response("", "claude-3-opus-20240229")
    assert "Error: Prompt cannot be empty." in response
    if mock_anthropic_client_fixture: # mock_client from fixture
        mock_anthropic_client_fixture.messages.create.assert_not_called()

def test_get_llm_response_api_error(mock_anthropic_client_fixture): # Use fixture
    mock_client = mock_anthropic_client_fixture
    if not mock_client:
        pytest.skip("Anthropic client mock not available.")

    mock_client.messages.create.side_effect = claude_handler.anthropic.APIConnectionError(request=MagicMock())
    prompt = "Test prompt for API error"
    model_name = "claude-3-opus-20240229"
    response = claude_handler.get_llm_response(prompt, model_name)
    assert "Error: Could not connect to Anthropic API." in response

def test_get_llm_response_rate_limit_error(mock_anthropic_client_fixture): # Use fixture
    mock_client = mock_anthropic_client_fixture
    if not mock_client:
        pytest.skip("Anthropic client mock not available.")

    # anthropic.RateLimitError now requires 'body' argument in constructor if response is provided.
    # Ensure response is a MagicMock that can provide a 'status_code' if needed by the error handler.
    mock_response = MagicMock()
    mock_response.status_code = 429 # Example status code for rate limit
    mock_client.messages.create.side_effect = claude_handler.anthropic.RateLimitError(message="Rate limit", response=mock_response, body=None)
    prompt = "Test prompt for rate limit"
    model_name = "claude-3-opus-20240229"
    response = claude_handler.get_llm_response(prompt, model_name)
    assert "Error: Anthropic API rate limit exceeded." in response

def test_get_llm_response_authentication_error(mock_anthropic_client_fixture): # Use fixture
    mock_client = mock_anthropic_client_fixture
    if not mock_client:
        pytest.skip("Anthropic client mock not available.")

    mock_response_auth = MagicMock()
    mock_response_auth.status_code = 401 # Example status code for auth error
    mock_client.messages.create.side_effect = claude_handler.anthropic.AuthenticationError(message="Auth error", response=mock_response_auth, body=None)
    prompt = "Test prompt for auth error"
    model_name = "claude-3-opus-20240229"
    response = claude_handler.get_llm_response(prompt, model_name)
    assert "Error: Anthropic API authentication failed." in response

def test_get_llm_response_generic_exception(mock_anthropic_client_fixture): # Use fixture
    mock_client = mock_anthropic_client_fixture
    if not mock_client:
        pytest.skip("Anthropic client mock not available.")

    mock_client.messages.create.side_effect = Exception("Some generic error")
    prompt = "Test prompt for generic error"
    model_name = "claude-3-opus-20240229"
    response = claude_handler.get_llm_response(prompt, model_name)
    assert "Error: An unexpected error occurred while contacting Anthropic." in response

@patch.object(claude_handler, 'client', None)
def test_get_llm_response_client_is_none():
    response = claude_handler.get_llm_response("Any prompt", "Any model")
    assert "Anthropic client is not initialized. Check API key." in response

def test_api_key_is_mocked_for_anthropic():
    assert ANTHROPIC_API_KEY == "test_anthropic_key" or ANTHROPIC_API_KEY is None

def test_get_llm_response_no_content_blocks(mock_anthropic_client_fixture): # Use fixture
    mock_client = mock_anthropic_client_fixture
    if not mock_client:
        pytest.skip("Anthropic client mock not available.")

    mock_api_response = MagicMock()
    mock_api_response.content = [] # No content blocks
    mock_client.messages.create.return_value = mock_api_response

    prompt = "Test prompt for no content blocks"
    model_name = "claude-3-opus-20240229"
    response = claude_handler.get_llm_response(prompt, model_name)
    assert "Error: Anthropic API returned no content." in response

def test_get_llm_response_no_text_in_content_blocks(mock_anthropic_client_fixture): # Use fixture
    mock_client = mock_anthropic_client_fixture
    if not mock_client:
        pytest.skip("Anthropic client mock not available.")

    mock_api_response = MagicMock()
    mock_image_block = MagicMock() # Simulate a non-text block
    mock_image_block.type = "image"
    mock_api_response.content = [mock_image_block]
    mock_client.messages.create.return_value = mock_api_response

    prompt = "Test prompt for non-text content block"
    model_name = "claude-3-opus-20240229"
    response = claude_handler.get_llm_response(prompt, model_name)
    assert "Error: Anthropic API returned no text content." in response

def test_get_llm_response_multiple_text_blocks_concatenated(mock_anthropic_client_fixture): # Use fixture
    mock_client = mock_anthropic_client_fixture
    if not mock_client:
        pytest.skip("Anthropic client mock not available.")

    mock_api_response = MagicMock()
    block1 = MagicMock(); block1.type = "text"; block1.text = "Hello "
    block2 = MagicMock(); block2.type = "text"; block2.text = "World!"
    block3 = MagicMock(); block3.type = "tool_use"; # Ignored
    mock_api_response.content = [block1, block3, block2]
    mock_client.messages.create.return_value = mock_api_response

    response = claude_handler.get_llm_response("Test prompt", "claude-3-sonnet-20240229")
    assert response == "Hello World!"
