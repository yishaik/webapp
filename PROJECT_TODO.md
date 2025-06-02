# Project TODO List

This document outlines the necessary tasks to complete the Prompt Builder & Optimizer application, based on `GUIDELINES.md` and `README.md`.

## Section 1: Core Backend Features

-   [ ] **User Authentication (Design and Implementation)**
    -   [ ] Design authentication mechanism (e.g., basic auth, JWT tokens).
    -   [ ] Implement user registration and login endpoints.
    -   [ ] Integrate authentication middleware with FastAPI.
    -   [ ] Update `Users` table in `backend/models.py` if necessary.
-   [ ] **Dynamic Questionnaire Logic (Generation and Storage)**
    -   [ ] Design algorithm for generating context-aware questions based on initial prompt.
    -   [ ] Implement backend logic to serve dynamic questions.
    -   [ ] Implement endpoints to store user responses to questionnaire (`QuestionnaireResponses` table).
-   [ ] **Prompt Optimization Engine (Core Algorithm)**
    -   [ ] Research and define optimization strategies for each supported LLM (OpenAI, Claude, Grok, Gemini).
    -   [ ] Implement a modular optimization engine in the backend.
    -   [ ] Allow for model-specific optimization parameters.
-   [ ] **Model Recommendation Logic**
    -   [ ] Design logic to suggest suitable models based on prompt content, task type, and desired outcome.
    -   [ ] Implement backend endpoint to provide model recommendations.

## Section 2: API Integrations

-   [ ] **Anthropic (Claude) API Handler**
    -   [ ] Implement API client for Anthropic models (Claude Opus 4, Claude Sonnet 4).
    -   [ ] Add necessary error handling and data parsing.
-   [ ] **xAI (Grok) API Handler**
    -   [ ] Implement API client for xAI models (Grok-3, Grok-3 Mini).
    -   [ ] Add necessary error handling and data parsing.
-   [ ] **Google Gemini API Handler**
    -   [ ] Implement API client for Google Gemini models (Gemini 2.5 Pro, Gemini 2.5 Flash).
    -   [ ] Add necessary error handling and data parsing.
-   [ ] **OpenAI API Handler (Review & Enhance)**
    -   [ ] Review existing OpenAI integration (if any beyond placeholder).
    -   [ ] Ensure it supports specified models (GPT-4.1, GPT-4.1 Mini, GPT-4.1 Nano) and features.
-   [ ] **Secure API Key Management**
    -   [ ] Implement secure loading of API keys from environment variables (`.env` file).
    -   [ ] Ensure keys are not exposed in logs or frontend.

## Section 3: Frontend Development

-   [ ] **Full Model Selection and Multi-Model Output Comparison UI**
    -   [ ] Enhance `ModelSelector.js` to dynamically list and select all supported models.
    -   [ ] Design and implement UI in `Results.js` (or new component) for side-by-side comparison of LLM outputs.
    -   [ ] Integrate with backend to fetch results from multiple models.
-   [ ] **Questionnaire Display and Interaction**
    -   [ ] Develop frontend components to display dynamic questionnaire questions.
    -   [ ] Implement logic to send user's answers to the backend.
-   [ ] **History Display and Navigation**
    -   [ ] Design UI for displaying past prompts, questionnaire responses, and model outputs.
    -   [ ] Implement components to fetch and render historical data from the backend.
    -   [ ] Allow users to select and reload past interactions.

## Section 4: Database and Persistence

-   [ ] **CRUD operations for `Prompts` table**
    -   [ ] Ensure backend has full CRUD operations for managing base prompts.
-   [ ] **CRUD operations for `QuestionnaireResponses` table**
    -   [ ] Ensure backend has full CRUD operations for questionnaire responses, linked to prompts.
-   [ ] **CRUD operations for `ModelOutputs` table**
    -   [ ] Ensure backend has full CRUD operations for model outputs, linked to prompts and specific models.
-   [ ] **Full Interaction History Management**
    -   [ ] Design and implement backend logic to save and retrieve complete interaction cycles (base prompt, questionnaire, selected models, outputs).
    -   [ ] Ensure proper foreign key relationships are utilized.

## Section 5: Testing

-   [ ] **Setup Unit Testing Framework (Backend)**
    -   [ ] Integrate `pytest` into the backend.
    -   [ ] Configure test database if necessary.
-   [ ] **Write Initial Backend Unit Tests**
    -   [ ] Write tests for core API endpoints (e.g., prompt submission, questionnaire logic).
    -   [ ] Write tests for prompt optimization logic.
-   [ ] **Setup Unit Testing Framework (Frontend)**
    -   [ ] Integrate Jest and React Testing Library (RTL) into the frontend.
-   [ ] **Write Initial Frontend Unit Tests**
    -   [ ] Write tests for key components (e.g., `PromptInput.js`, `ModelSelector.js`, `Results.js`).
-   [ ] **Setup Integration Testing Framework**
    -   [ ] Plan strategy for integration tests (e.g., testing frontend-backend interaction).

## Section 6: Deployment

-   [ ] **Create `Dockerfile` for Backend**
    -   [ ] Write Dockerfile to containerize the FastAPI application.
    -   [ ] Include all necessary dependencies and configurations.
-   [ ] **Create `Dockerfile` for Frontend**
    -   [ ] Write Dockerfile to build and serve the React application (e.g., using Nginx).
-   [ ] **Create `docker-compose.yml`**
    -   [ ] Define services for backend, frontend, and potentially the database.
    -   [ ] Configure networking and volume mounts for Raspberry Pi deployment.

## Section 7: Documentation & Review

-   [ ] **Review and Clarify `CLAUDE.md`**
    -   [ ] Determine the purpose of `CLAUDE.md`.
    -   [ ] Integrate any relevant information into the main GUIDELINES or API integration tasks.
    -   [ ] Remove or archive `CLAUDE.md` if redundant.
-   [ ] **Update `README.md`**
    -   [ ] As features are implemented, update `README.md` with current status, new setup instructions, or usage details.
    -   [ ] Ensure API documentation link is accurate.
-   [ ] **Environment Variable Documentation**
    -   [ ] Clearly document all required environment variables in `.env.example` and `README.md`.
