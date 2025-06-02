# Core Backend TODO

**Last Updated: 2025-06-02**

**Status:** All core backend tasks listed below appear to be **completed** based on the information in `README.md`. This document primarily serves as a historical reference unless new core backend tasks are identified.

## Previously Listed Tasks (Considered Completed):

### User Authentication (Basic Auth)
-   **Task:** Implement basic authentication middleware in FastAPI, define hardcoded credentials, protect endpoints.
    -   **Status:** Completed. `README.md` confirms "Basic Authentication: Protects application endpoints" and details the hardcoded credentials in `backend/security.py`.
-   **Task:** Create a `User` model if needed or remove if stateless.
    -   **Status:** Completed. Basic auth implemented is stateless, so an explicit User model for this purpose is not required.

### Dynamic Questionnaire Logic
-   **Task:** Design algorithm and implement FastAPI endpoints (`/generate_questionnaire`, `/submit_questionnaire`) for a dynamic questionnaire.
    -   **Status:** Completed. `README.md` feature list includes "Adaptive Questionnaire: Generates 3-5 context-aware questions..." and "Prompt History & Persistence" for responses.

### Prompt Optimization Engine
-   **Task:** Research strategies, implement `backend/prompt_optimizer.py` module, and create a FastAPI endpoint (`/optimize_prompt`).
    -   **Status:** Completed. `README.md` feature list includes "Prompt Optimization Engine: Refines your base prompt and questionnaire answers..."

### Model Recommendation Logic
-   **Task:** Design rule-based logic and implement a FastAPI endpoint (`/recommend_models`) for model recommendations.
    -   **Status:** Completed. `README.md` feature list includes "Model Recommendations: Suggests suitable models..."

## Future Considerations:
- If new core backend features are planned, they should be documented here.
- Enhancements to existing features (e.g., moving auth credentials to `.env`, more advanced optimization strategies) could be listed as new tasks if prioritized.