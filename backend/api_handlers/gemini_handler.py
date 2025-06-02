import google.generativeai as genai
from backend.config import GOOGLE_API_KEY, logging

if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
else:
    logging.warning("Google Gemini client not configured due to missing GOOGLE_API_KEY.")

def get_llm_response(prompt: str, model_name: str) -> str:
    """
    Gets a response from a Google Gemini model.

    Args:
        prompt: The prompt to send to the model.
        model_name: The specific Gemini model to use (e.g., "gemini-1.5-pro-latest").

    Returns:
        The model's text response, or an error message string.
    """
    if not GOOGLE_API_KEY: # Check if API key was loaded for genai.configure
        error_msg = "Google Gemini client is not configured. Check GOOGLE_API_KEY."
        logging.error(error_msg)
        return f"Error: {error_msg}"
    if not prompt:
        logging.warning("Google Gemini handler received an empty prompt.")
        return "Error: Prompt cannot be empty."

    try:
        logging.info(f"Sending request to Google Gemini model: {model_name} with prompt (first 50 chars): '{prompt[:50]}...'")

        model = genai.GenerativeModel(model_name)
        # The generate_content method can take various types of input.
        # For simple text prompt, just passing the string is fine.
        response = model.generate_content(prompt)

        if response.parts:
            # Concatenate text from all parts, though typically there's one for simple prompts.
            response_text = "".join(part.text for part in response.parts if hasattr(part, 'text'))
            if response_text:
                logging.info(f"Received response from Google Gemini model {model_name} (first 50 chars): '{response_text[:50]}...'")
                return response_text.strip()
            else:
                # This case might occur if response.parts exist but none have 'text' or text is empty.
                # Or if response.text (shortcut for single part) is empty.
                logging.warning(f"Google Gemini API call for model {model_name} returned parts but no text.")
                return "Error: Google Gemini API returned no text content."
        elif hasattr(response, 'text') and response.text: # Check response.text directly
             logging.info(f"Received response from Google Gemini model {model_name} (first 50 chars): '{response.text[:50]}...'")
             return response.text.strip()
        else:
            # This path might be taken if the response object itself is unusual or empty.
            # Also, check for prompt_feedback for safety reasons.
            if response.prompt_feedback and response.prompt_feedback.block_reason:
                block_reason = response.prompt_feedback.block_reason
                logging.warning(f"Google Gemini API call for model {model_name} was blocked. Reason: {block_reason}")
                return f"Error: Prompt blocked by Google Gemini API. Reason: {block_reason}"
            logging.warning(f"Google Gemini API call for model {model_name} returned no parts or text.")
            return "Error: Google Gemini API returned no parsable content."

    except Exception as e:
        # The google-generativeai SDK might raise various specific exceptions.
        # For simplicity, catching a general Exception, but more specific handling can be added.
        # Example: google.api_core.exceptions.PermissionDenied for API key issues after configuration.
        # Example: google.api_core.exceptions.ResourceExhausted for rate limits.
        logging.error(f"An unexpected error occurred with Google Gemini API: {e}", exc_info=True)
        # Attempt to provide a more user-friendly message for common issues if possible
        if "API_KEY_INVALID" in str(e) or "PermissionDenied" in str(e):
             return f"Error: Google Gemini API authentication failed. Check your API key. Details: {e}"
        if "RateLimit" in str(e) or "ResourceExhausted" in str(e):
             return f"Error: Google Gemini API rate limit exceeded. Please try again later. Details: {e}"
        return f"Error: An unexpected error occurred while contacting Google Gemini. {e}"

# Example Usage:
# if __name__ == "__main__":
#     if not GOOGLE_API_KEY:
#         print("Please set your GOOGLE_API_KEY in a .env file in the backend directory to test.")
#     else:
#         test_prompt = "What are some interesting facts about the planet Jupiter?"
#         # Actual model name from GEMINI_API_INSTRUCTIONS.md
#         model = "gemini-1.5-flash-latest"
#         print(f"Testing Google Gemini model: {model}")
#         response = get_llm_response(test_prompt, model)
#         print(f"Prompt: {test_prompt}")
#         print(f"Response: {response}")

#         print("\nTesting with an empty prompt:")
#         response_empty = get_llm_response("", model)
#         print(f"Response to empty prompt: {response_empty}")

#         # Test for blocked prompt (example, might not trigger actual blocking)
#         # blocked_prompt = "Tell me something inappropriate."
#         # print(f"\nTesting potentially blocked prompt with Gemini model: {model}")
#         # response_blocked = get_llm_response(blocked_prompt, model)
#         # print(f"Response to blocked prompt: {response_blocked}")
