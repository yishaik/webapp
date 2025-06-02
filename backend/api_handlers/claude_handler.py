import anthropic
from backend.config import ANTHROPIC_API_KEY, logging

if ANTHROPIC_API_KEY:
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
else:
    client = None
    logging.warning("Anthropic client not initialized due to missing API key.")

def get_llm_response(prompt: str, model_name: str) -> str:
    """
    Gets a response from an Anthropic Claude model.

    Args:
        prompt: The prompt to send to the model.
        model_name: The specific Claude model to use (e.g., "claude-3-opus-20240229").

    Returns:
        The model's text response, or an error message string.
    """
    if not client:
        error_msg = "Anthropic client is not initialized. Check API key."
        logging.error(error_msg)
        return f"Error: {error_msg}"
    if not prompt:
        logging.warning("Anthropic handler received an empty prompt.")
        return "Error: Prompt cannot be empty."

    try:
        logging.info(f"Sending request to Anthropic model: {model_name} with prompt (first 50 chars): '{prompt[:50]}...'")

        # Anthropic API uses a 'messages' structure.
        # Max tokens to generate; adjust as needed.
        response = client.messages.create(
            model=model_name,
            max_tokens=4096, # Max output tokens as per ANTHROPIC_API_INSTRUCTIONS.md
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        if response.content and len(response.content) > 0:
            # Assuming the first block of content is the primary text response
            response_text = ""
            for block in response.content:
                if block.type == "text":
                    response_text += block.text

            if response_text:
                logging.info(f"Received response from Anthropic model {model_name} (first 50 chars): '{response_text[:50]}...'")
                return response_text.strip()
            else:
                logging.warning(f"Anthropic API call for model {model_name} returned content but no text block.")
                return "Error: Anthropic API returned no text content."
        else:
            logging.warning(f"Anthropic API call for model {model_name} returned no content.")
            return "Error: Anthropic API returned no content."

    except anthropic.APIConnectionError as e:
        logging.error(f"Anthropic API connection error: {e}")
        return f"Error: Could not connect to Anthropic API. {e}"
    except anthropic.RateLimitError as e:
        logging.error(f"Anthropic API rate limit exceeded: {e}")
        return f"Error: Anthropic API rate limit exceeded. Please try again later. {e}"
    except anthropic.AuthenticationError as e:
        logging.error(f"Anthropic API authentication error: {e}")
        return f"Error: Anthropic API authentication failed. Check your API key. {e}"
    except anthropic.APIStatusError as e:
        logging.error(f"Anthropic API status error (code {e.status_code}): {e.response}")
        return f"Error: Anthropic API returned an error (status {e.status_code}). {e.message}"
    except Exception as e:
        logging.error(f"An unexpected error occurred with Anthropic API: {e}", exc_info=True)
        return f"Error: An unexpected error occurred while contacting Anthropic. {e}"

# Example Usage:
# if __name__ == "__main__":
#     if not ANTHROPIC_API_KEY:
#         print("Please set your ANTHROPIC_API_KEY in a .env file in the backend directory to test.")
#     else:
#         test_prompt = "Explain the concept of emergence in complex systems."
#         # Actual model name from ANTHROPIC_API_INSTRUCTIONS.md
#         model = "claude-3-sonnet-20240229"
#         print(f"Testing Anthropic model: {model}")
#         response = get_llm_response(test_prompt, model)
#         print(f"Prompt: {test_prompt}")
#         print(f"Response: {response}")

#         print("\nTesting with an empty prompt:")
#         response_empty = get_llm_response("", model)
#         print(f"Response to empty prompt: {response_empty}")
