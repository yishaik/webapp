# Frontend TODO

This file outlines tasks for the frontend development (React.js with Tailwind CSS) of the Prompt Builder & Optimizer application.

## Initial Setup (if not already done)

-   [ ] Ensure `frontend` directory has a React project initialized (e.g., with Create React App or Vite).
-   [ ] Install Tailwind CSS and configure it for the project.
-   [ ] Install `axios` or use `fetch` for API calls.

## Core UI Components

-   **`App.js` (Main Layout)**
    -   [ ] Setup basic page structure (e.g., header, main content area, footer).
    -   [ ] Implement routing if needed for different views (e.g., main interaction page, history page).
-   **`PromptInput.js`**
    -   [ ] Create a component with a textarea for users to input their base prompt.
    -   [ ] Add a submit button to send the prompt to the backend (to trigger questionnaire generation).
-   **`Questionnaire.js`**
    -   [ ] Create a component to display questions received from the backend.
    -   [ ] For each question, provide an input field (e.g., text input, radio buttons if applicable).
    -   [ ] Add a submit button to send answers to the backend.
-   **`ModelSelector.js`**
    -   [ ] Create a component to display available LLMs (names fetched from backend or hardcoded initially based on `GUIDELINES.md`).
    -   [ ] Allow users to select one or more models to run the optimized prompt against.
        *   Models: OpenAI (GPT-4.1, Mini, Nano), Anthropic (Claude Opus 4, Sonnet 4), xAI (Grok-3, Mini), Google (Gemini 2.5 Pro, Flash).
-   **`Results.js` (or similar for multi-model output)**
    -   [ ] Design and implement a UI to display outputs from selected LLMs side-by-side.
    -   [ ] Clearly label which output belongs to which model.
    -   [ ] Handle loading states while waiting for API responses.
-   **`ModelRecommendations.js`**
    -   [ ] Create a component to display model recommendations received from the backend.

## Frontend Logic and API Interaction

-   **API Service Module (`frontend/src/services/api.js` or similar)**
    -   [ ] Create functions to interact with all necessary backend endpoints:
        *   Submit initial prompt, get questionnaire.
        *   Submit questionnaire answers.
        *   Get model recommendations.
        *   Get optimized prompt (or this happens implicitly via model response endpoint).
        *   Request model responses for selected models.
        *   Fetch history (see below).
-   **State Management (e.g., React Context or a lightweight state library)**
    -   [ ] Manage application state: current prompt, questionnaire, answers, selected models, results, loading states, errors.

## Full Model Selection and Multi-Model Output Comparison UI

-   [ ] Enhance `ModelSelector.js` to dynamically list all supported models (ideally fetched from a backend config endpoint).
-   [ ] Ensure `Results.js` can gracefully handle and display multiple model outputs simultaneously.
-   [ ] Implement logic to call the backend for each selected model and update the UI as results arrive.

## Questionnaire Display and Interaction

-   [ ] Ensure `Questionnaire.js` can dynamically render questions of different types if the backend supports it (e.g., text, multiple choice).
-   [ ] Implement frontend logic to collect answers and send them to the `/submit_questionnaire` backend endpoint.

## History Display and Navigation

-   **`HistoryView.js` (or a new page/section)**
    -   [ ] Design UI to display a list of past interactions (e.g., base prompt, date).
    -   [ ] Implement component(s) to fetch historical data from the backend (endpoint to be defined in `TODO_DATABASE.md`).
    -   [ ] Allow users to click on a past interaction to view its details (prompt, questionnaire, selected models, outputs).
    -   [ ] (Optional) Allow users to select and reload a past interaction into the main interface.

## Styling and User Experience

-   [ ] Apply Tailwind CSS classes for a clean, responsive, and user-friendly interface.
-   [ ] Add appropriate loading indicators and error messages. 