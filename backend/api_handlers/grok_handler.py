import openai # xAI uses an OpenAI-compatible API
from backend.config import XAI_API_KEY, logging

# Initialize the xAI client using OpenAI's SDK structure
if XAI_API_KEY:
    client = openai.OpenAI(
        api_key=XAI_API_KEY,
        base_url="https://api.x.ai/v1"
    )
else:
    client = None
    logging.warning("xAI (Grok) client not initialized due to missing XAI_API_KEY.")

def get_llm_response(prompt: str, model_name: str) -> str:
    """
    Gets a response from an xAI Grok model.

    Args:
        prompt: The prompt to send to the model.
        model_name: The specific Grok model to use (e.g., "grok-3", "grok-3-mini").

    Returns:
        The model's text response, or an error message string.
    """
    if not client:
        error_msg = "xAI (Grok) client is not initialized. Check XAI_API_KEY."
        logging.error(error_msg)
        return f"Error: {error_msg}"
    if not prompt:
        logging.warning("xAI (Grok) handler received an empty prompt.")
        return "Error: Prompt cannot be empty."

    try:
        logging.info(f"Sending request to xAI Grok model: {model_name} with prompt (first 50 chars): '{prompt[:50]}...'")

        completion = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "user", "content": prompt}
            ]
            # max_tokens can be specified if needed, e.g., max_tokens=8192 for grok-3 as per XAI_API_INSTRUCTIONS
        )

        if completion.choices and len(completion.choices) > 0:
            response_text = completion.choices[0].message.content
            logging.info(f"Received response from xAI Grok model {model_name} (first 50 chars): '{response_text[:50]}...'")
            return response_text.strip() if response_text else ""
        else:
            logging.warning(f"xAI Grok API call for model {model_name} returned no choices or empty response.")
            return "Error: xAI Grok API returned no response or empty content."

    # xAI uses OpenAI's error types when using their SDK compatibility
    except openai.APIConnectionError as e:
        logging.error(f"xAI Grok API connection error: {e}")
        return f"Error: Could not connect to xAI Grok API. {e}"
    except openai.RateLimitError as e:
        logging.error(f"xAI Grok API rate limit exceeded: {e}")
        return f"Error: xAI Grok API rate limit exceeded. Please try again later. {e}"
    except openai.AuthenticationError as e:
        logging.error(f"xAI Grok API authentication error: {e}")
        return f"Error: xAI Grok API authentication failed. Check your API key. {e}"
    except openai.APIStatusError as e:
        logging.error(f"xAI Grok API status error (code {e.status_code}): {e.response}")
        return f"Error: xAI Grok API returned an error (status {e.status_code}). {e.message}"
    except Exception as e:
        logging.error(f"An unexpected error occurred with xAI Grok API: {e}", exc_info=True)
        return f"Error: An unexpected error occurred while contacting xAI Grok. {e}"

# Example Usage:
# if __name__ == "__main__":
#     if not XAI_API_KEY:
#         print("Please set your XAI_API_KEY in a .env file in the backend directory to test.")
#     else:
#         test_prompt = "What is the airspeed velocity of an unladen swallow?"
#         # Actual model name from XAI_API_INSTRUCTIONS.md
#         model = "grok-3-mini" # or "grok-3"
#         print(f"Testing xAI Grok model: {model}")
#         response = get_llm_response(test_prompt, model)
#         print(f"Prompt: {test_prompt}")
#         print(f"Response: {response}")

#         print("\nTesting with an empty prompt:")
#         response_empty = get_llm_response("", model)
#         print(f"Response to empty prompt: {response_empty}")
