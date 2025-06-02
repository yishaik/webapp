# Core Backend TODO

This file outlines tasks for the core backend features of the Prompt Builder & Optimizer application.

## User Authentication (Basic Auth)

-   [ ] Implement basic authentication middleware in FastAPI.
    *   Define a single, hardcoded username/password initially (can be moved to `.env`).
    *   Protect all relevant API endpoints.
-   [ ] Create a simple `User` model in `backend/models.py` (id, username) if needed for session management, or remove if basic auth is stateless.
    *   *Note: `GUIDELINES.md` mentions a `Users` table with `id`, `username`, `email`. Re-evaluate if email is needed for basic auth in a single-user app. For now, assume simpler model.*

## Dynamic Questionnaire Logic

-   [ ] Design an algorithm to generate 3-5 simple, context-aware questions based on the initial prompt's keywords or length.
    *   Example: If prompt is short, ask for desired length. If prompt mentions "code", ask about programming language.
-   [ ] Implement a FastAPI endpoint (e.g., `/generate_questionnaire`) that takes an initial prompt and returns a list of questions.
-   [ ] Implement a FastAPI endpoint (e.g., `/submit_questionnaire`) to store user responses.
    *   This will link to the `QuestionnaireResponses` table (covered in `TODO_DATABASE.md`).

## Prompt Optimization Engine

-   [ ] Research and define 1-2 simple, generic optimization strategies applicable across most LLMs (e.g., adding role-playing, asking for step-by-step thinking, specifying output format).
-   [ ] Implement a Python module (`backend/prompt_optimizer.py`) with a function that takes an initial prompt, questionnaire answers, and a target model (enum/string) and returns an optimized prompt string.
-   [ ] Allow the optimization function to accept model-specific parameters in the future (placeholder for now).
-   [ ] Implement a FastAPI endpoint (e.g., `/optimize_prompt`) that uses this engine.

## Model Recommendation Logic

-   [ ] Design a simple rule-based logic to suggest 1-2 suitable models.
    *   Example: If prompt mentions "creative writing", suggest Opus. If "quick summary", suggest Flash/Mini. If "coding", suggest Opus/Grok.
-   [ ] Implement a FastAPI endpoint (e.g., `/recommend_models`) that takes the initial prompt and questionnaire context, and returns a list of recommended model names. 