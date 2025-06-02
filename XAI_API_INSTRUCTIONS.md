# xAI (Grok) API Instructions

This document provides instructions and examples for using the xAI API (Grok), based on the provided documentation snippets. The xAI API is designed for compatibility with OpenAI and Anthropic SDKs.

For more details, refer to the [official xAI documentation](https://docs.x.ai/) and their guide on [Migration from Other Providers](https://docs.x.ai/docs/migration-from-other-providers).

## Key Features:

*   **Compatibility:** Easily use the xAI API by making minimal changes if you are already using OpenAI or Anthropic SDKs.
*   **Models:** Access xAI models like Grok-3 and Grok-3 Mini (ensure you specify the correct model name in your requests).

## Using with OpenAI SDK:

To use the xAI API with the OpenAI Python SDK, you need to:

1.  Initialize the `OpenAI` client.
2.  Set your `api_key` to your XAI_API_KEY.
3.  Set the `base_url` to `"https://api.x.ai/v1"`.
4.  Specify an xAI model name (e.g., `"grok-3"`, `"grok-3-mini"`) in your API requests.

**Python Example (OpenAI SDK):**

```python
from openai import OpenAI

# Ensure your XAI_API_KEY is set as an environment variable or passed directly
# client = OpenAI(
#   api_key="YOUR_XAI_API_KEY", 
#   base_url="https://api.x.ai/v1",
# )

# Assuming XAI_API_KEY is an environment variable:
client = OpenAI(
  api_key=os.environ.get("XAI_API_KEY"), # Replace with your actual key if not using env var
  base_url="https://api.x.ai/v1",
)

# Example chat completion (adapt as needed for other functionalities):
# response = client.chat.completions.create(
#   model="grok-3-mini", # Or other xAI model
#   messages=[
#     {"role": "user", "content": "Explain the importance of large language models."}
#   ]
# )
# print(response.choices[0].message.content)
```
*Note: The example above is a common use case. Adapt the method call (e.g., `client.completions.create` for older models/APIs or other specific tasks) and parameters based on the OpenAI SDK version and your specific needs.* Access to `os.environ` might be restricted, ensure your API key is securely managed.

## Using with Anthropic SDK:

To use the xAI API with the Anthropic Python SDK, you need to:

1.  Initialize the `Anthropic` client.
2.  Set your `api_key` to your XAI_API_KEY.
3.  Set the `base_url` to `"https://api.x.ai"`.
4.  Specify an xAI model name in your API requests.

**Python Example (Anthropic SDK):**

```python
from anthropic import Anthropic

# Ensure your XAI_API_KEY is set as an environment variable or passed directly
# client = Anthropic(
#   api_key="YOUR_XAI_API_KEY", 
#   base_url="https://api.x.ai",
# )

# Assuming XAI_API_KEY is an environment variable:
client = Anthropic(
  api_key=os.environ.get("XAI_API_KEY"), # Replace with your actual key if not using env var
  base_url="https://api.x.ai",
)

# Example message creation (adapt as needed):
# response = client.messages.create(
#    model="grok-3-mini", # Or other xAI model
#    max_tokens=1024,
#    messages=[
#        {
#            "role": "user",
#            "content": "Explain the concept of zero-shot prompting.",
#        }
#    ]
# )
# print(response.content)
```
*Note: The example above is a common use case. Adapt parameters based on the Anthropic SDK version and your specific needs.* Access to `os.environ` might be restricted, ensure your API key is securely managed.

## Important Considerations:

*   **API Key:** Securely manage your `XAI_API_KEY`. It's recommended to use environment variables.
*   **Model Names:** Always use the correct model identifiers provided by xAI in your API calls (e.g., `grok-3`, `grok-3-mini`).
*   **SDK Capabilities:** The xAI API is designed for compatibility but be aware of capabilities not offered by the respective OpenAI or Anthropic SDKs, or differences in how features are implemented. Refer to xAI documentation for any caveats.

## Questions and Feedback:

For any questions or feedback, contact xAI support at `support@x.ai`. 