# Testing TODO

This file outlines tasks for setting up testing frameworks and writing tests for the Prompt Builder & Optimizer application.

## Backend Testing (Python/FastAPI with `pytest`)

-   **Setup `pytest` Framework**
    -   [ ] Add `pytest` and `httpx` (for testing FastAPI endpoints) to `backend/requirements.txt` (or `requirements-dev.txt`).
    -   [ ] Create a `backend/tests` directory.
    -   [ ] Configure `pytest` (e.g., `pytest.ini` or `pyproject.toml`) if necessary.
    -   [ ] Setup a test database configuration (e.g., in-memory SQLite or a separate test DB file) for tests that interact with the database. Ensure test data is isolated and cleaned up.

-   **Write Initial Backend Unit Tests (`backend/tests/unit`)**
    -   [ ] **Test Core Logic:**
        *   Write tests for the dynamic questionnaire generation logic (`backend/ ... /questionnaire_logic.py` or similar).
        *   Write tests for the prompt optimization engine (`backend/prompt_optimizer.py`).
        *   Write tests for the model recommendation logic.
    -   [ ] **Test API Handlers (Mocks):**
        *   Write tests for individual API handlers (`backend/api_handlers/*_handler.py`), mocking external API calls to avoid actual network requests during unit tests.
    -   [ ] **Test CRUD Operations:**
        *   Write tests for database CRUD operations (`backend/crud.py`) using the test database.

-   **Write Initial Backend Integration Tests (`backend/tests/integration`)**
    -   [ ] **Test API Endpoints:**
        *   Write tests for core API endpoints (e.g., `/generate_questionnaire`, `/submit_questionnaire`, `/optimize_prompt`, `/recommend_models`, `/get_model_response`) using `httpx` to make requests to the test client.
        *   Ensure endpoints correctly interact with services, CRUD operations, and return expected responses/status codes.
        *   Test protected endpoints with and without authentication.

## Frontend Testing (React with Jest & React Testing Library)

-   **Setup Jest and React Testing Library (RTL)**
    -   [ ] Ensure Jest and RTL are set up in the `frontend` project (usually included with Create React App, or need manual setup with Vite).
    -   [ ] Add any necessary Jest configuration (e.g., `frontend/jest.config.js` or in `package.json`).
    -   [ ] Setup mock service worker (`msw`) or similar to mock API calls in frontend tests.

-   **Write Initial Frontend Unit Tests (`frontend/src/components/.../__tests__` or `frontend/src/tests/unit`)**
    -   [ ] **Test Key Components:**
        *   Write tests for `PromptInput.js`: rendering, input changes, submission.
        *   Write tests for `ModelSelector.js`: rendering options, selection changes.
        *   Write tests for `Results.js`: rendering different states (loading, error, data), displaying multiple outputs.
        *   Write tests for `Questionnaire.js`: rendering questions, handling answers.
    -   [ ] **Test Utility Functions/Hooks:**
        *   Write tests for any custom hooks or utility functions (e.g., API service call functions, state manipulation logic).

## Integration Testing Strategy (Overall)

-   [ ] Plan a strategy for end-to-end integration tests (e.g., using tools like Cypress or Playwright if full browser testing is desired later, or focusing on frontend-backend API interaction tests for now).
    *   *For current scope, focus on backend integration tests with `httpx` and frontend component tests mocking backend calls.*

## General Testing Practices

-   [ ] Aim for good test coverage of critical application logic.
-   [ ] Ensure tests are independent and can be run in any order.
-   [ ] Add test commands to `README.md` (e.g., `cd backend && pytest`, `cd frontend && npm test`). 