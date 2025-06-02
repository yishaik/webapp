# PromptForge: LLM Prompt Engineering Toolkit

PromptForge is a web application designed to help users craft, optimize, and test prompts for major language models. It supports OpenAI (GPT series), Anthropic (Claude series), xAI (Grok series), and Google (Gemini series) models, providing a streamlined workflow for prompt engineering.

## Features

- **Dynamic Prompt Input**: Easy-to-use interface for submitting your initial prompt idea.
- **Adaptive Questionnaire**: Generates 3-5 context-aware questions based on your initial prompt to gather specific requirements and constraints.
- **Multi-Model Interaction**: Simultaneously send prompts to various supported LLMs.
    - OpenAI: GPT-4.1, GPT-4.1 Mini, GPT-4.1 Nano (mapped to actual SDK models like gpt-4o, gpt-4-turbo, gpt-3.5-turbo).
    - Anthropic: Claude Opus 4, Claude Sonnet 4.
    - xAI: Grok-3, Grok-3 Mini.
    - Google: Gemini 2.5 Pro, Gemini 2.5 Flash.
- **Model Recommendations**: Suggests suitable models based on the prompt's content and questionnaire answers.
- **Prompt Optimization Engine**: Refines your base prompt and questionnaire answers into an optimized prompt tailored for LLM interaction, incorporating strategies like role-playing and step-by-step thinking.
- **Side-by-Side Results**: View and compare responses from different LLMs in a clear, organized interface.
- **Prompt History & Persistence**: Saves all prompts, questionnaire responses, and model outputs to a local SQLite database for review and reuse.
- **Dockerized Deployment**: Easy setup and deployment using Docker Compose for both backend and frontend services.
- **Basic Authentication**: Protects application endpoints.

## Tech Stack

- **Frontend**: React.js with Tailwind CSS, using `axios` for API calls and `react-router-dom` for routing.
- **Backend**: Python with FastAPI, using `SQLModel` for ORM and Pydantic for data validation.
- **Database**: SQLite for persistent storage.
- **API Handlers**: Custom handlers for OpenAI, Anthropic, xAI (Grok), and Google Gemini SDKs.
- **Containerization**: Docker & Docker Compose.
- **Web Server (Frontend)**: Nginx (serving the static React build).

## Quick Start: Docker Deployment

This application is designed to be run with Docker Compose.

### Prerequisites
1.  **Docker and Docker Compose:** Ensure Docker and Docker Compose are installed on your system.
2.  **Backend Environment File:**
    *   Navigate to the `backend/` directory.
    *   Copy the example environment file: `cp .env.example .env`
    *   Edit `backend/.env` and fill in your actual API keys for the LLM services you intend to use.
        ```
        OPENAI_API_KEY="your_openai_api_key_here"
        ANTHROPIC_API_KEY="your_anthropic_api_key_here"
        XAI_API_KEY="your_xai_api_key_here"
        GOOGLE_API_KEY="your_google_api_key_here"
        ```

### Running the Application
1.  Navigate to the project root directory (where `docker-compose.yml` is located).
2.  Build and start the services in detached mode:
    ```bash
    docker-compose up -d --build
    ```
    *   `--build`: Forces Docker to rebuild images if there are changes.
    *   `-d`: Runs containers in the background.

### Accessing the Application
-   **Frontend UI**: Open your browser and go to `http://localhost:3000`
-   **Backend API Docs (Swagger UI)**: `http://localhost:8000/docs`

### Viewing Logs
To view logs from the running containers:
```bash
docker-compose logs -f
```
Or for a specific service (e.g., `backend` or `frontend`):
```bash
docker-compose logs -f backend
```

### Stopping the Application
To stop the services:
```bash
docker-compose down
```
To stop services and remove volumes (including the database, use with caution):
```bash
docker-compose down -v
```

## Environment Variables & Configuration

### API Keys
-   As mentioned in the "Quick Start", API keys for LLM services (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `XAI_API_KEY`, `GOOGLE_API_KEY`) **must** be defined in `backend/.env`. Refer to `backend/.env.example`.

### Basic Authentication
-   The application uses Basic HTTP Authentication for all its API endpoints.
-   For simplicity in this version, credentials are hardcoded directly in `backend/security.py`:
    -   Username: `admin`
    -   Password: `password123`
-   To change these, you would need to modify the `HARDCODED_USERNAME` and `HARDCODED_PASSWORD` variables in that file and rebuild the backend Docker image. For a production environment, consider moving these to environment variables as well.

## Project Structure

-   `docker-compose.yml`: Defines and configures the multi-container Docker application.
-   `backend/`: Contains the Python FastAPI backend application.
    -   `Dockerfile`: For building the backend Docker image.
    -   `.env.example`: Template for API keys.
    -   `main.py`: FastAPI application entry point.
    -   `api_handlers/`: Modules for interacting with different LLM SDKs.
    -   `tests/`: Backend unit and integration tests.
-   `frontend/`: Contains the React.js frontend application.
    -   `Dockerfile`: For building the frontend Docker image (multi-stage with Nginx).
    -   `nginx.conf`: Nginx configuration for serving the SPA.
    -   `src/`: Frontend source code.
    -   `src/services/api.js`: Module for making API calls to the backend.
    -   `src/mocks/`: MSW (Mock Service Worker) setup for frontend tests.

## Data Persistence

-   The backend service uses a named Docker volume (`prompts_db_volume`) to persist the SQLite database file (`prompts.db`). This ensures that your prompt history and other data are retained even if the backend container is stopped and restarted.

## Running Tests

### Backend Tests
Ensure the Docker services are running or use a local Python environment with dev dependencies installed.
To run backend tests using Docker Compose:
```bash
docker-compose exec backend pytest tests/
```
To run specific tests:
```bash
docker-compose exec backend pytest tests/unit/test_crud.py
docker-compose exec backend pytest tests/integration/test_main_api.py
```
Alternatively, if you have a local development setup for the backend:
```bash
cd backend
# (activate virtualenv if using one)
pip install -r requirements.txt # Ensure test dependencies like pytest are installed
pytest tests/
```

### Frontend Tests
To run frontend tests using Docker Compose (if your frontend image's entrypoint allows it, or add a test script to package.json that Docker can run):
```bash
# This command assumes your frontend container has a shell and npm installed globally for this execution context.
# A more common approach is to run tests locally or as part of a CI step that has Node.js.
# docker-compose exec frontend npm test

# Recommended: Run frontend tests in your local Node.js environment:
cd frontend
npm install # Ensure dev dependencies like msw are installed
npm test
```

This `README.md` provides a comprehensive overview for users and developers.
If you encounter any issues, please check the logs or open an issue in the repository.