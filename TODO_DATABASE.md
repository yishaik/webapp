# Database and Persistence TODO

**Last Updated: 2025-06-02**

**Status:** All database and persistence tasks listed below appear to be **completed** based on the information in `README.md`. This document primarily serves as a historical reference unless new database-related tasks are identified.

## Previously Listed Tasks (Considered Completed):

### Database Setup
-   **Task:** Choose ORM, configure SQLite (`prompts.db`), implement auto table creation.
    -   **Status:** Completed. `README.md` confirms `SQLModel` as the ORM, SQLite for persistence (`prompts.db`), and the application's functionality implies table creation is handled.

### Data Models (`backend/models.py`)
-   **Task:** Define `User` (optional/simplified), `Prompt`, `QuestionnaireResponse`, and `ModelOutput` models.
    -   **Status:** Completed. `README.md`'s "Prompt History & Persistence" feature confirms the necessity and implementation of `Prompt`, `QuestionnaireResponse`, and `ModelOutput` models. The `User` model was considered optional for the described basic auth.

### CRUD Operations (`backend/crud.py` or similar)
-   **Task:** Implement CRUD helper functions for all models and define Pydantic schemas (`backend/schemas.py`).
    -   **Status:** Completed. The "Prompt History & Persistence" feature, use of Pydantic, and mention of `tests/unit/test_crud.py` in `README.md` confirm these are implemented.

### Full Interaction History Management
-   **Task:** Implement FastAPI endpoints for retrieving interaction history and ensure correct data linking (e.g., `Prompt` to `QuestionnaireResponse` and `ModelOutput`).
    -   **Status:** Completed. `README.md`'s "Prompt History & Persistence" and "Side-by-Side Results" features confirm these capabilities. The application's workflow necessitates the described data linking logic.

## Future Considerations:
- If database schema migrations become necessary (e.g., using Alembic with SQLModel), that would be a new task.
- Enhancements to data querying or new data models for additional features would be documented here.