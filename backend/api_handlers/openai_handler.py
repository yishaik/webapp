import openai
from backend.config import OPENAI_API_KEY, logging

# Initialize the OpenAI client
# It's good practice to initialize it once if the key doesn't change often.
# However, if the key could change during runtime or for different requests (not the case here),
# then initialization might need to be inside the function or managed differently.
if OPENAI_API_KEY:
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
else:
    client = None
    logging.warning("OpenAI client not initialized due to missing API key.")

def get_llm_response(prompt: str, model_name: str) -> str:
    """
    Gets a response from an OpenAI model.

    Args:
        prompt: The prompt to send to the model.
        model_name: The specific OpenAI model to use (e.g., "gpt-4o", "gpt-4-turbo").

    Returns:
        The model's text response, or an error message string.
    """
    if not client:
        error_msg = "OpenAI client is not initialized. Check API key."
        logging.error(error_msg)
        return f"Error: {error_msg}"
    if not prompt:
        logging.warning("OpenAI handler received an empty prompt.")
        return "Error: Prompt cannot be empty."

    try:
        logging.info(f"Sending request to OpenAI model: {model_name} with prompt (first 50 chars): '{prompt[:50]}...'")

        # Using the ChatCompletion endpoint as it's the standard for current models
        completion = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        # Extract the response text
        # Assuming we want the content of the first choice's message
        if completion.choices and len(completion.choices) > 0:
            response_text = completion.choices[0].message.content
            logging.info(f"Received response from OpenAI model {model_name} (first 50 chars): '{response_text[:50]}...'")
            return response_text.strip() if response_text else ""
        else:
            logging.warning(f"OpenAI API call for model {model_name} returned no choices or empty response.")
            return "Error: OpenAI API returned no response or empty content."

    except openai.APIConnectionError as e:
        logging.error(f"OpenAI API connection error: {e}")
        return f"Error: Could not connect to OpenAI API. {e}"
    except openai.RateLimitError as e:
        logging.error(f"OpenAI API rate limit exceeded: {e}")
        return f"Error: OpenAI API rate limit exceeded. Please try again later. {e}"
    except openai.AuthenticationError as e:
        logging.error(f"OpenAI API authentication error: {e}")
        return f"Error: OpenAI API authentication failed. Check your API key. {e}"
    except openai.APIStatusError as e:
        logging.error(f"OpenAI API status error (code {e.status_code}): {e.response}")
        return f"Error: OpenAI API returned an error (status {e.status_code}). {e.message}"
    except Exception as e:
        logging.error(f"An unexpected error occurred with OpenAI API: {e}", exc_info=True)
        # It's important to log exc_info=True for unexpected errors to get the traceback
        return f"Error: An unexpected error occurred while contacting OpenAI. {e}"

# Example Usage (for testing this handler directly)
# if __name__ == "__main__":
#     if not OPENAI_API_KEY:
#         print("Please set your OPENAI_API_KEY in a .env file in the backend directory to test.")
#     else:
#         test_prompt = "Translate 'Hello, world!' into French."
#         # Referencing actual model names, e.g., "gpt-3.5-turbo" or "gpt-4o"
#         # The friendly names like "GPT-4.1" will be mapped in main.py
#         model = "gpt-3.5-turbo" # Or use "gpt-4o" if available and key supports it
#         print(f"Testing OpenAI model: {model}")
#         response = get_llm_response(test_prompt, model)
#         print(f"Prompt: {test_prompt}")
#         print(f"Response: {response}")

#         print("\nTesting with an empty prompt:")
#         response_empty = get_llm_response("", model)
#         print(f"Response to empty prompt: {response_empty}")

#         # To test error handling, you could temporarily use an invalid API key or model name
#         # print("\nTesting with an invalid API key (requires manual change or temp env var):")
#         # temp_client_invalid_key = openai.OpenAI(api_key="invalid_key")
#         # original_client = client # to restore later
#         # client = temp_client_invalid_key
#         # response_auth_error = get_llm_response(test_prompt, model)
#         # print(f"Response to auth error: {response_auth_error}")
#         # client = original_client # restore client

#         print("\nTesting with potentially unsupported model (example):")
#         response_invalid_model = get_llm_response(test_prompt, "gpt-nonexistent-model")
#         print(f"Response to invalid model: {response_invalid_model}")
