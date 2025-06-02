# Database and Persistence TODO

This file outlines tasks for setting up the SQLite database, defining models, and implementing CRUD operations for the Prompt Builder & Optimizer application.

## Database Setup

-   [ ] Choose a Python ORM: `SQLModel` (recommended for FastAPI) or `SQLAlchemy`.
-   [ ] Configure the SQLite database connection in the backend (e.g., `database.py`). The database file should be `prompts.db` as per `SECURITY.md`.
-   [ ] Implement logic to create database tables based on models if they don't exist upon application startup.

## Data Models (`backend/models.py`)

Define the following models based on `GUIDELINES.md`, using the chosen ORM:

-   **`User` Model** (Simplified for basic auth, re-evaluate necessity as per `TODO_CORE_BACKEND.md`)
    -   `id` (Primary Key, Integer)
    -   `username` (String, unique)
    -   *(Note: `email` field from `GUIDELINES.md` might be omitted for simple single-user basic auth)*

-   **`Prompt` Model**
    -   `id` (Primary Key, Integer)
    -   `user_id` (Foreign Key to `User.id`, nullable if User model is very simple/optional)
    -   `base_prompt` (Text)
    -   `timestamp` (DateTime, default to current time)
    -   Relationships:
        *   One-to-many with `QuestionnaireResponse`
        *   One-to-many with `ModelOutput`

-   **`QuestionnaireResponse` Model**
    -   `id` (Primary Key, Integer)
    -   `prompt_id` (Foreign Key to `Prompt.id`)
    -   `question` (Text)
    -   `answer` (Text)
    -   Relationships:
        *   Many-to-one with `Prompt`

-   **`ModelOutput` Model**
    -   `id` (Primary Key, Integer)
    -   `prompt_id` (Foreign Key to `Prompt.id`)
    -   `model_name` (String, e.g., "claude-opus-4", "gpt-4.1")
    -   `output` (Text)
    -   `timestamp` (DateTime, default to current time)
    -   Relationships:
        *   Many-to-one with `Prompt`

## CRUD Operations (`backend/crud.py` or similar)

For each model, implement helper functions for Create, Read, Update, Delete operations. These will be used by API endpoints.

-   **`User` CRUD** (if User model is implemented)
    -   `create_user(db: Session, user: UserCreateSchema) -> User`
    -   `get_user(db: Session, user_id: int) -> User | None`
    -   `get_user_by_username(db: Session, username: str) -> User | None`
    -   *(Update/Delete might not be needed for a single-user app with hardcoded basic auth)*

-   **`Prompt` CRUD**
    -   `create_prompt(db: Session, prompt: PromptCreateSchema, user_id: int | None) -> Prompt`
    -   `get_prompt(db: Session, prompt_id: int) -> Prompt | None`
    -   `get_prompts_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> list[Prompt]`
    -   `update_prompt(...)` (if prompts can be edited after creation)
    -   `delete_prompt(...)` (if prompts can be deleted)

-   **`QuestionnaireResponse` CRUD**
    -   `create_questionnaire_response(db: Session, response: QuestionnaireResponseCreateSchema, prompt_id: int) -> QuestionnaireResponse`
    -   `create_multiple_questionnaire_responses(db: Session, responses: list[QuestionnaireResponseCreateSchema], prompt_id: int) -> list[QuestionnaireResponse]`
    -   `get_questionnaire_responses_by_prompt(db: Session, prompt_id: int) -> list[QuestionnaireResponse]`

-   **`ModelOutput` CRUD**
    -   `create_model_output(db: Session, output: ModelOutputCreateSchema, prompt_id: int) -> ModelOutput`
    -   `get_model_outputs_by_prompt(db: Session, prompt_id: int) -> list[ModelOutput]`

-   **Pydantic Schemas (`backend/schemas.py`)**
    -   Define Pydantic schemas for request and response data validation for all models (e.g., `PromptCreate`, `PromptRead`, `ModelOutputCreate`, etc.).

## Full Interaction History Management

-   **Backend Logic/Endpoints for History**
    -   [ ] Design and implement FastAPI endpoint(s) to retrieve complete interaction cycles:
        *   An endpoint to list all prompts (e.g., `/history/prompts`) with basic info (ID, base_prompt preview, timestamp).
        *   An endpoint to get full details for a specific prompt ID (e.g., `/history/prompt/{prompt_id}`), which returns the `Prompt` object along with its related `QuestionnaireResponse` and `ModelOutput` objects.
    -   [ ] Ensure proper foreign key relationships are utilized and data is fetched efficiently (e.g., using SQLAlchemy joined loading).
-   [ ] The `/submit_questionnaire` endpoint should create a `Prompt` entry first, then link `QuestionnaireResponse` entries to it.
-   [ ] The `/get_model_response` endpoint should link `ModelOutput` entries to the relevant `Prompt`. 