import pytest
from unittest.mock import patch, MagicMock
from backend.api_handlers import gemini_handler
from backend.config import GOOGLE_API_KEY # To check if it's mocked

# Fixture to mock the genai.GenerativeModel instance and genai.configure
@pytest.fixture(autouse=True)
def patch_gemini_client_and_configure():
    # Mock genai.configure to prevent it from actually trying to configure with a real key during tests
    with patch.object(gemini_handler.genai, 'configure') as mock_configure:
        # Mock the GenerativeModel instance
        mock_model_instance = MagicMock()
        mock_model_instance.generate_content = MagicMock() # This is what get_llm_response calls

        # Mock genai.GenerativeModel to return our mock_model_instance
        with patch.object(gemini_handler.genai, 'GenerativeModel', return_value=mock_model_instance) as mock_generative_model_class:
            yield {
                "mock_configure": mock_configure,
                "mock_generative_model_class": mock_generative_model_class,
                "mock_model_instance": mock_model_instance
            }

def test_get_llm_response_success(patch_gemini_client_and_configure):
    mock_model_instance = patch_gemini_client_and_configure["mock_model_instance"]

    mock_response_text = "Test Gemini response"
    mock_api_response = MagicMock()

    # Simulate Gemini's response structure (list of parts with text attribute)
    mock_part = MagicMock()
    mock_part.text = mock_response_text
    mock_api_response.parts = [mock_part]
    mock_api_response.prompt_feedback = None # No blocking

    # If response.text is accessed directly (older versions or simple cases)
    # mock_api_response.text = mock_response_text

    mock_model_instance.generate_content.return_value = mock_api_response

    prompt = "Test prompt for Gemini"
    model_name = "gemini-1.5-pro-latest"
    response = gemini_handler.get_llm_response(prompt, model_name)

    patch_gemini_client_and_configure["mock_generative_model_class"].assert_called_once_with(model_name)
    mock_model_instance.generate_content.assert_called_once_with(prompt)
    assert response == mock_response_text

def test_get_llm_response_empty_prompt(patch_gemini_client_and_configure):
    response = gemini_handler.get_llm_response("", "gemini-1.5-pro-latest")
    assert "Error: Prompt cannot be empty." in response
    patch_gemini_client_and_configure["mock_model_instance"].generate_content.assert_not_called()


def test_get_llm_response_api_error_generic(patch_gemini_client_and_configure):
    mock_model_instance = patch_gemini_client_and_configure["mock_model_instance"]
    mock_model_instance.generate_content.side_effect = Exception("Some generic SDK error")

    prompt = "Test prompt for API error"
    model_name = "gemini-1.5-pro-latest"
    response = gemini_handler.get_llm_response(prompt, model_name)
    assert "Error: An unexpected error occurred while contacting Google Gemini." in response

def test_get_llm_response_permission_denied_error(patch_gemini_client_and_configure):
    mock_model_instance = patch_gemini_client_and_configure["mock_model_instance"]
    # Simulate a permission denied error string, as the actual exception class might vary
    mock_model_instance.generate_content.side_effect = Exception("API_KEY_INVALID or PermissionDenied")

    prompt = "Test prompt for auth error"
    model_name = "gemini-1.5-pro-latest"
    response = gemini_handler.get_llm_response(prompt, model_name)
    assert "Error: Google Gemini API authentication failed." in response


# To test the "client not configured" case, we need to simulate GOOGLE_API_KEY being None
# This requires a bit more care due to how genai.configure works at module load time.
@patch.object(gemini_handler, 'GOOGLE_API_KEY', None) # Patch the KEY *within the handler module*
@patch.object(gemini_handler.genai, 'configure') # Still mock configure to avoid real calls
def test_get_llm_response_client_not_configured(mock_genai_configure_again):
    # We also need to ensure that genai.GenerativeModel is not called if key is None.
    # The current structure of get_llm_response checks GOOGLE_API_KEY first.
    response = gemini_handler.get_llm_response("Any prompt", "Any model")
    assert "Google Gemini client is not configured. Check GOOGLE_API_KEY." in response
    mock_genai_configure_again.assert_not_called() # configure shouldn't be called if key is missing

def test_api_key_is_mocked_for_gemini():
    # This checks the key from the main config, which is patched by conftest.py
    assert GOOGLE_API_KEY == "test_google_key" or GOOGLE_API_KEY is None

def test_get_llm_response_blocked_prompt(patch_gemini_client_and_configure):
    mock_model_instance = patch_gemini_client_and_configure["mock_model_instance"]

    mock_api_response = MagicMock()
    mock_api_response.parts = [] # No useful parts
    mock_api_response.text = None  # No direct text

    # Simulate a blocked prompt feedback
    mock_feedback = MagicMock()
    mock_feedback.block_reason = "SAFETY"
    mock_api_response.prompt_feedback = mock_feedback

    mock_model_instance.generate_content.return_value = mock_api_response

    prompt = "Potentially problematic prompt"
    model_name = "gemini-1.5-flash-latest"
    response = gemini_handler.get_llm_response(prompt, model_name)
    assert "Error: Prompt blocked by Google Gemini API. Reason: SAFETY" in response

def test_get_llm_response_no_text_in_parts(patch_gemini_client_and_configure):
    mock_model_instance = patch_gemini_client_and_configure["mock_model_instance"]

    mock_api_response = MagicMock()
    # Simulate a part that isn't text or has no text attribute
    non_text_part = MagicMock()
    # del non_text_part.text # Ensure it has no text attribute or it's None
    # setattr(non_text_part, 'text', None) # More explicit if needed
    mock_api_response.parts = [non_text_part]
    mock_api_response.text = None
    mock_api_response.prompt_feedback = None


    mock_model_instance.generate_content.return_value = mock_api_response

    prompt = "Test for non-text part"
    model_name = "gemini-1.5-flash-latest"
    response = gemini_handler.get_llm_response(prompt, model_name)
    assert "Error: Google Gemini API returned no parsable content." in response # Or "no text content" depending on path

def test_get_llm_response_empty_response_text(patch_gemini_client_and_configure):
    mock_model_instance = patch_gemini_client_and_configure["mock_model_instance"]

    mock_api_response = MagicMock()
    mock_part = MagicMock(); mock_part.text = "  "; # Whitespace only
    mock_api_response.parts = [mock_part]
    mock_api_response.prompt_feedback = None

    mock_model_instance.generate_content.return_value = mock_api_response
    response = gemini_handler.get_llm_response("Test", "gemini-1.5-flash-latest")
    assert response == "" # Should be stripped to empty string

    mock_part.text = "" # Empty string
    mock_api_response.parts = [mock_part]
    mock_model_instance.generate_content.return_value = mock_api_response
    response_empty = gemini_handler.get_llm_response("Test", "gemini-1.5-flash-latest")
    assert response_empty == ""
