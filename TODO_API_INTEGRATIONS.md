# API Integrations TODO

This file outlines tasks for integrating various Language Model (LLM) APIs into the backend.

## Secure API Key Management

-   [ ] Create `backend/.env.example` with placeholders for all required API keys (OpenAI, Anthropic, xAI, Google).
-   [ ] Implement logic in the backend (e.g., in a `config.py` or `main.py`) to load API keys from a `backend/.env` file using a library like `python-dotenv`.
-   [ ] Ensure API keys are never hardcoded or logged.
-   [ ] Add `backend/.env` to `.gitignore` (confirm it's already there from `SECURITY.md`).

## API Handler Implementation (General Structure for each LLM)

For each LLM (Anthropic, xAI, Google, OpenAI), create a dedicated Python module (e.g., `backend/api_handlers/claude_handler.py`). Each handler should:

-   [ ] Implement a function to make API calls to the specific LLM.
    *   Accepts prompt, model name (e.g., "Claude Opus 4", "gpt-4.1-mini"), and any necessary parameters.
    *   Retrieves the API key securely.
    *   Returns the LLM's response text.
-   [ ] Implement basic error handling (e.g., API errors, network issues) and log errors appropriately (without exposing sensitive data).
-   [ ] Implement simple data parsing to extract the relevant text output from the API response.

## Anthropic (Claude) API Handler

-   [ ] **Module**: `backend/api_handlers/claude_handler.py`
-   [ ] Implement API client for Anthropic models (Claude Opus 4, Claude Sonnet 4) using the general structure above.

## xAI (Grok) API Handler

-   [ ] **Module**: `backend/api_handlers/grok_handler.py`
-   [ ] Implement API client for xAI models (Grok-3, Grok-3 Mini) using the general structure above.

## Google Gemini API Handler

-   [ ] **Module**: `backend/api_handlers/gemini_handler.py`
-   [ ] Implement API client for Google Gemini models (Gemini 2.5 Pro, Gemini 2.5 Flash) using the general structure above.

## OpenAI API Handler (Review & Enhance)

-   [ ] **Module**: `backend/api_handlers/openai_handler.py` (or existing module)
-   [ ] Review any existing OpenAI integration for completeness and adherence to the general handler structure.
-   [ ] Ensure it supports the specified models (GPT-4.1, GPT-4.1 Mini, GPT-4.1 Nano).
-   [ ] Enhance error handling and data parsing if necessary.

## Unified API Interaction Endpoint

-   [ ] Create a FastAPI endpoint (e.g., `/get_model_response`) that:
    *   Accepts `prompt_id` (or initial prompt + questionnaire data), `model_name` (e.g., "claude-opus-4", "gpt-4.1").
    *   Retrieves/generates the optimized prompt.
    *   Routes the request to the appropriate LLM API handler based on `model_name`.
    *   Stores the output using the `ModelOutputs` CRUD operations (covered in `TODO_DATABASE.md`).
    *   Returns the model's response to the frontend. 