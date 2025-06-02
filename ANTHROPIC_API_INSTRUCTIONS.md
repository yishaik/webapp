# Anthropic (Claude) API Instructions

This document provides a summary of instructions, best practices, and capabilities for the Anthropic Claude API, based on the provided documentation snippets. For detailed SDK usage and the most up-to-date examples, please refer to the [official Anthropic Documentation](https://docs.anthropic.com/).

## General Implementation Lifecycle with Claude:

The documentation outlines an 8-step process for implementing Claude:

1.  **Scope your use case:** Identify the problem and define requirements (features, performance, cost).
2.  **Design your integration:** Select Claude's capabilities (e.g., vision, tool use) and models (Opus, Sonnet, Haiku). Choose a deployment method (Anthropic API, AWS Bedrock, Vertex AI).
3.  **Prepare your data:** Identify and clean relevant data for Claude's context.
4.  **Develop your prompts:** Use tools like Workbench to create evals, draft, and iteratively refine prompts.
5.  **Implement Claude:** Set up your environment, integrate Claude with your systems (APIs, databases, UIs), define human-in-the-loop requirements.
6.  **Test your system:** Conduct red teaming and A/B testing.
7.  **Deploy to production:** Deploy when the application runs smoothly.
8.  **Monitor and improve:** Continuously monitor performance and make improvements.

## Key Capabilities & Models:

*   **Models:** Claude Opus, Claude Sonnet, Claude Haiku. The choice depends on the task's complexity, performance, and cost requirements.
*   **Capabilities:** Vision, tool use, text generation, summarization, coding, etc.
*   **Deployment Options:** Anthropic API, AWS Bedrock, Google Cloud Vertex AI.

## Prompt Engineering & Best Practices:

*   **Be Explicit:** Clearly describe the desired behavior and output format.
*   **Add Context:** Provide relevant information to improve performance.
*   **Use Examples & Details:** Be vigilant with examples and details in your prompts.
*   **Control Response Format:** Specify the format you expect.
*   **Leverage Thinking & Interleaved Thinking:** Encourage step-by-step reasoning.
*   **Keep Claude "In Character":** Use system prompts to define a role and rules for interaction, especially for enterprise-grade assistants. For example:
    ```
    System: You are AcmeBot, the enterprise-grade AI assistant for AcmeTechCo. Your role: - Analyze technical documents... - Maintain a professional, concise tone
    User: Here is the user query... Your rules for interaction are: - Always reference AcmeTechCo standards... - If unsure, ask for clarification...
    Assistant (prefill): [AcmeBot]
    ```
*   **Claude 4 Specifics (migrating from Sonnet 3.7 or for best results):
    *   Be specific about desired behavior.
    *   Frame instructions with modifiers that encourage quality and detail (e.g., "Include as many relevant features... Go beyond the basics...").
    *   Request specific features like animations or interactive elements explicitly.

## Handling Specific Use Cases (e.g., Legal Summarization):

*   **Ensure no liability:** Include disclaimers for AI-generated summaries.
*   **Handle diverse document types:** Ensure your data pipeline can convert various file formats (PDF, Word, text).
*   **Parallelize API calls:** For large document collections, make parallel API calls to Claude, respecting rate limits.

## Using the Anthropic Python SDK (General Example Structure):

Below is a general structure. Refer to the [official Anthropic documentation](https://docs.anthropic.com/en/api/client-sdks) for detailed Python SDK examples.

1.  **Installation:**
    ```bash
    pip install anthropic
    ```

2.  **Initialization & Usage:**
    Set your `ANTHROPIC_API_KEY` as an environment variable or pass it directly.

    **Python Example (Conceptual - check official docs for specifics):**
    ```python
    from anthropic import Anthropic
    import os

    # It's recommended to set your API key as an environment variable:
    # export ANTHROPIC_API_KEY='your-api-key'

    # client = Anthropic()
    # or, if not using environment variable for the key:
    # client = Anthropic(api_key="YOUR_ANTHROPIC_API_KEY")

    # Assuming ANTHROPIC_API_KEY is an environment variable:
    client = Anthropic(
        api_key=os.environ.get("ANTHROPIC_API_KEY") # Replace with your actual key if not using env var
    )

    # Example: Message Creation (using a model like claude-3-opus-20240229)
    # try:
    #     response = client.messages.create(
    #         model="claude-3-opus-20240229", # Or other Claude model
    #         max_tokens=1000,
    #         system="You are a helpful research assistant.", # Optional system prompt
    #         messages=[
    #             {"role": "user", "content": "What are the latest advancements in quantum computing?"}
    #         ]
    #     )
    #     print(response.content)
    # except Exception as e:
    #    print(f"An error occurred: {e}")
    ```
    *Note: The exact model names, parameters, and methods (e.g., `client.messages.create`) depend on the Anthropic SDK version. Always consult the latest official Anthropic documentation.* Access to `os.environ` might be restricted, ensure your API key is securely managed.

## Important Considerations:

*   **API Key Management:** Securely manage your `ANTHROPIC_API_KEY`.
*   **Rate Limits:** Be aware of API rate limits.
*   **Workbench Tool:** Use Anthropic's Workbench for prompt development and evaluation.

Refer to the [Anthropic documentation](https://docs.anthropic.com/) for comprehensive guides, API references, and SDK information. 