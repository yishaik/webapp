# Testing TODO

**Last Updated: 2025-06-02**

**Status:** Testing frameworks for both backend (`pytest`) and frontend (Jest/RTL with MSW) are **set up and operational**. `README.md` includes instructions for running tests. Initial unit and integration tests exist. The focus moving forward is on increasing test coverage and maintaining tests as the application evolves.

## Backend Testing (Python/FastAPI with `pytest`)

-   **`pytest` Framework Setup**
    -   **Status:** Completed.
    -   **Details:** `pytest` and `httpx` are included in backend dependencies. `backend/tests` directory is structured with `unit` and `integration` subdirectories. Test database configuration is in place, as evidenced by `tests/unit/test_crud.py`. `README.md` provides commands to run these tests.

-   **Backend Unit Tests (`backend/tests/unit`)**
    -   **Status:** Initial tests implemented; ongoing effort for comprehensive coverage.
    -   **Details:** `tests/unit/test_crud.py` exists.
    -   **Ongoing:** Continuously add unit tests for:
        *   Core logic (dynamic questionnaire, prompt optimizer, model recommender).
        *   API handlers (mocking external calls).
        *   Other utility functions and modules.

-   **Backend Integration Tests (`backend/tests/integration`)**
    -   **Status:** Initial tests implemented; ongoing effort for comprehensive coverage.
    -   **Details:** `tests/integration/test_main_api.py` exists.
    -   **Ongoing:** Continuously add integration tests for:
        *   All API endpoints, covering various scenarios and request parameters.
        *   Interactions between services.
        *   Authentication and authorization for protected endpoints.

## Frontend Testing (React with Jest & React Testing Library)

-   **Jest and React Testing Library (RTL) Setup**
    -   **Status:** Completed.
    -   **Details:** Frontend testing setup is operational, using Jest/RTL. `msw` is configured for mocking API calls, as indicated in `frontend/src/mocks/`. `README.md` provides commands to run frontend tests.

-   **Frontend Unit/Component Tests (`frontend/src/components/.../__tests__` or `frontend/src/tests/unit`)**
    -   **Status:** Setup complete; ongoing effort for comprehensive coverage.
    -   **Details:** The framework for frontend tests is in place.
    -   **Ongoing:** Continuously add tests for:
        *   Key components (e.g., `PromptInput.js`, `ModelSelector.js`, `Results.js`, `Questionnaire.js`).
        *   Custom hooks and utility functions.
        *   User interactions and state changes within components.

## Integration Testing Strategy (Overall)

-   **Current Strategy:**
    -   Backend: API integration tests using `pytest` and `httpx` to directly test FastAPI endpoints and their interaction with backend services.
    -   Frontend: Component-level tests using Jest/RTL, with API interactions mocked using `msw`. This focuses on testing component behavior in isolation or in controlled integration with mocked services.
-   **Future Considerations (Optional):**
    -   True end-to-end (E2E) testing with tools like Cypress or Playwright could be considered if more comprehensive browser-based testing is required. This is not currently in scope.

## General Testing Practices (Ongoing Guidelines)

-   **Test Coverage:** Strive for good test coverage of critical application logic in both frontend and backend.
-   **Test Independence:** Ensure tests are independent and can be run in any order without affecting each other.
-   **Maintainability:** Write clear, concise, and maintainable tests.
-   **`README.md` Test Commands:** Completed. Test execution commands are documented in `README.md`.