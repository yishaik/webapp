# MASTERPLAN.md

This document outlines a suggested order for completing the TODO files, details missing parts, and provides suggestions for future improvements for the Prompt Builder & Optimizer application.

## Phase 1: Core Backend and API Foundations

**Objective:** Establish the fundamental backend services, API integrations, and database structure.

1.  **`TODO_CORE_BACKEND.md` (Partially - Authentication & Basic Endpoints)**
    *   **Priority:** High
    *   **Tasks:**
        *   Implement basic FastAPI setup.
        *   Implement basic authentication (hardcoded initially is fine as per `TODO_CORE_BACKEND.md`).
        *   Define initial Pydantic schemas for basic request/response.
    *   **Rationale:** Essential for any interaction with the application.

2.  **`TODO_DATABASE.md` (Initial Setup & Core Models)**
    *   **Priority:** High
    *   **Tasks:**
        *   Set up SQLite and ORM (`SQLModel` or `SQLAlchemy`).
        *   Define `Prompt`, `QuestionnaireResponse`, `ModelOutput` models.
        *   Implement basic CRUD operations for these core models.
        *   The `User` model can be simplified or deferred if sticking to single-user basic auth for now (as hinted in `TODO_DATABASE.md` and `TODO_CORE_BACKEND.md`).
    *   **Rationale:** Data persistence is crucial for application functionality and history.

3.  **`TODO_API_INTEGRATIONS.md` (API Key Management & One Handler)**
    *   **Priority:** High
    *   **Tasks:**
        *   Implement secure API key management (`backend/.env.example`, loading keys).
        *   Implement the handler for *one* LLM API (e.g., OpenAI or Anthropic) as a template.
        *   Define the unified API interaction endpoint (`/get_model_response`) structure, even if it only calls one handler initially.
    *   **Rationale:** Core functionality involves LLM interaction. Getting one API working proves the concept.

## Phase 2: Basic Frontend and Core Logic Implementation

**Objective:** Create a minimal viable product (MVP) with one end-to-end flow.

4.  **`TODO_FRONTEND.md` (Basic UI for one flow)**
    *   **Priority:** Medium-High
    *   **Tasks:**
        *   Set up React project with Tailwind CSS.
        *   Implement `PromptInput.js`.
        *   Implement a simplified `ModelSelector.js` (can be hardcoded with the one LLM implemented in the backend).
        *   Implement `Results.js` to display output from the single LLM.
        *   Implement basic API service module to call backend endpoints developed in Phase 1.
    *   **Rationale:** Provides a user interface to test the backend functionality.

5.  **`TODO_CORE_BACKEND.md` (Questionnaire & Optimization - Basic Versions)**
    *   **Priority:** Medium
    *   **Tasks:**
        *   Implement a *very simple* version of dynamic questionnaire logic (e.g., 1-2 fixed questions).
        *   Implement endpoints `/generate_questionnaire` and `/submit_questionnaire`.
        *   Implement a *very simple* version of the prompt optimization engine (e.g., append a fixed phrase).
        *   Implement `/optimize_prompt` endpoint.
    *   **Rationale:** Fleshes out the core prompt enhancement loop.

6.  **`TODO_FRONTEND.md` (Integrate Questionnaire)**
    *   **Priority:** Medium
    *   **Tasks:**
        *   Implement `Questionnaire.js` to display and submit the basic questions.
        *   Integrate this flow with `PromptInput.js` and the submission to `Results.js`.
    *   **Rationale:** Completes the basic user interaction cycle.

## Phase 3: Expanding Functionality and Integrations

**Objective:** Add more LLM integrations, improve core logic, and enhance the frontend.

7.  **`TODO_API_INTEGRATIONS.md` (Remaining API Handlers)**
    *   **Priority:** Medium
    *   **Tasks:**
        *   Implement handlers for the remaining LLMs (xAI, Google, and the other of OpenAI/Anthropic).
        *   Ensure the unified API interaction endpoint (`/get_model_response`) correctly routes to all handlers.
    *   **Rationale:** Expands the core utility of the application.

8.  **`TODO_FRONTEND.md` (Full Model Selection & Multi-Model Output)**
    *   **Priority:** Medium
    *   **Tasks:**
        *   Enhance `ModelSelector.js` to dynamically list all supported models.
        *   Update `Results.js` to handle and display multiple model outputs.
        *   Implement logic to call the backend for each selected model.
    *   **Rationale:** Key feature for comparing LLM outputs.

9.  **`TODO_CORE_BACKEND.md` (Model Recommendation Logic - Basic)**
    *   **Priority:** Low-Medium
    *   **Tasks:**
        *   Implement a simple rule-based model recommendation logic.
        *   Implement `/recommend_models` endpoint.
    *   **Rationale:** Adds value by guiding the user.

10. **`TODO_FRONTEND.md` (Display Recommendations)**
    *   **Priority:** Low-Medium
    *   **Tasks:**
        *   Implement `ModelRecommendations.js`.
    *   **Rationale:** Makes backend recommendations visible.

## Phase 4: Testing, Documentation, and Deployment

**Objective:** Ensure application quality, provide good documentation, and prepare for deployment.

11. **`TODO_TESTING.md`**
    *   **Priority:** Medium-High (should be ongoing, but dedicated focus here)
    *   **Tasks:**
        *   Set up `pytest` for backend. Write unit and integration tests for core logic and API endpoints.
        *   Set up Jest/RTL for frontend. Write unit tests for key components.
        *   Focus on testing the core flow and API integrations.
    *   **Rationale:** Critical for application stability and maintainability.

12. **`TODO_DOCUMENTATION.md`**
    *   **Priority:** Medium
    *   **Tasks:**
        *   Update `README.md` with accurate setup, features, tech stack, and API docs link.
        *   Create/Update `.env.example` as per `SECURITY.md` and reconcile any discrepancies with `TODO_API_INTEGRATIONS.md` (root vs. `backend/.env.example`). Clarify and unify this.
        *   Document environment variable setup clearly.
    *   **Rationale:** Essential for usability and maintainability.

13. **`TODO_DEPLOYMENT.md`**
    *   **Priority:** Medium
    *   **Tasks:**
        *   Create Dockerfiles for backend and frontend.
        *   Create `docker-compose.yml`.
        *   Document Raspberry Pi deployment steps.
    *   **Rationale:** Fulfills the project goal of Raspberry Pi deployment.

## Phase 5: Advanced Features and Refinements

**Objective:** Add more sophisticated features and improve user experience.

14. **`TODO_DATABASE.md` (Full Interaction History)**
    *   **Priority:** Medium
    *   **Tasks:**
        *   Implement backend logic and endpoints for fetching full interaction history.
    *   **Rationale:** Enhances user value by allowing review of past work.

15. **`TODO_FRONTEND.md` (History Display)**
    *   **Priority:** Medium
    *   **Tasks:**
        *   Implement `HistoryView.js` to display and navigate interaction history.
    *   **Rationale:** Provides UI for the history feature.

16. **Refinements to `TODO_CORE_BACKEND.md`**
    *   **Priority:** Low-Medium
    *   **Tasks:**
        *   Improve dynamic questionnaire logic (more context-aware).
        *   Enhance prompt optimization engine (more strategies, model-specific).
        *   Refine model recommendation logic.
    *   **Rationale:** Iterative improvements to core intelligent features.

## Missing Parts & Future Improvements

### Missing Parts Identified from TODOs & Guidelines:

1.  **User Model/Authentication Scheme Clarification:**
    *   `GUIDELINES.md` mentions a `Users` table with `id, username, email`.
    *   `TODO_CORE_BACKEND.md` suggests a simpler model for basic auth and questions if email is needed.
    *   `TODO_DATABASE.md` also notes this simplification for basic auth.
    *   **Decision Needed:** For a single-user local app, a full `User` table with email might be overkill if basic auth is purely stateless or uses a hardcoded/env-var user. If any user-specific data *not* tied to a prompt needs storing, or if future multi-user capability is envisioned, then the richer `User` model is better. For now, the simplified approach seems fine.

2.  **`.env.example` Location:**
    *   `TODO_DOCUMENTATION.md` notes a discrepancy: `SECURITY.md` implies a root `.env.example`, while `TODO_API_INTEGRATIONS.md` suggests `backend/.env.example`.
    *   **Decision Needed:** A single root `.env.example` that `docker-compose` uses to populate `backend/.env` is cleaner, as suggested in `TODO_DOCUMENTATION.md`. This needs to be standardized.

3.  **Error Handling Details:**
    *   While `TODO_API_INTEGRATIONS.md` mentions basic error handling, specific error responses to the frontend (e.g., API key invalid, model unavailable, rate limits) should be defined for a better UX.

4.  **Frontend State Management:**
    *   `TODO_FRONTEND.md` mentions "React Context or a lightweight state library." A decision on the specific approach would be beneficial early in frontend development.

5.  **Configuration for Models:**
    *   `TODO_FRONTEND.md` suggests model names could be fetched from a backend config endpoint. This is a good idea for maintainability rather than hardcoding in the frontend. This endpoint isn't explicitly in a `TODO` but is a good addition.

### Suggestions for Future Improvements (Beyond current TODOs):

1.  **Advanced Prompt Optimization Techniques:**
    *   Explore more sophisticated optimization strategies (e.g., few-shot prompting, chain-of-thought, context stuffing based on model context window size).
    *   Allow users to select or customize optimization techniques.

2.  **Prompt Templates/Library:**
    *   Allow users to save and reuse successful prompt structures or templates.

3.  **Cost Estimation:**
    *   For APIs that charge per token, provide a rough cost estimate before sending a prompt (this is complex and requires token counting and pricing info).

4.  **Streaming Responses:**
    *   For LLMs that support streaming, update the frontend and backend to handle streamed responses for better perceived performance.

5.  **Vision/Multimodal Input in UI:**
    *   If models like Gemini or GPT-4 Vision are used, extend the UI to allow image uploads or other multimodal inputs. The `GEMINI_API_INSTRUCTIONS.md` and `OPENAI_API_INSTRUCTIONS.md` hint at these capabilities.

6.  **Detailed Model Capability Tags/Filters:**
    *   Beyond just names, tag models with capabilities (e.g., "strong reasoning," "creative," "coding," "multimodal") to help users select.

7.  **Export/Import Functionality:**
    *   Allow users to export their prompt history or import prompts.

8.  **UI/UX Enhancements:**
    *   Dark mode.
    *   More responsive design for various screen sizes (even if primarily for local Pi use).
    *   Loading skeletons or more detailed loading states.

9.  **Security Enhancements (if ever exposed beyond local network):**
    *   Move beyond basic auth.
    *   Input sanitization more robustly.
    *   Rate limiting on API endpoints.

10. **Version Control for Prompts:**
    *   If a user iterates on a base prompt multiple times, allow them to see versions or revert.

This master plan provides a structured approach. Flexibility will be needed as development progresses and new insights are gained.
Prioritize tasks that unblock other major components or deliver core functionality first. 