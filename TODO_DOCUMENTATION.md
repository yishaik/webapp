# Documentation & Review TODO

This file outlines tasks for maintaining project documentation and reviewing existing guideline files.


## Update `README.md`

-   [ ] **Review `README.md` for accuracy and completeness as features are implemented.**
-   [ ] **Quick Start / Setup Instructions:**
    -   [ ] Verify backend and frontend setup commands are correct and match `CLAUDE.md` if those are the source of truth for running locally.
    -   [ ] Add testing commands (`pytest`, `npm test`).
    -   [ ] Add Docker Compose deployment commands (e.g., `docker-compose up -d --build`).
-   [ ] **Features List:**
    -   [ ] Ensure it accurately reflects the implemented features.
-   [ ] **Tech Stack:**
    -   [ ] Confirm it matches `GUIDELINES.md` and actual implementation choices (e.g., React, FastAPI, SQLite, Tailwind CSS).
-   [ ] **API Documentation Link:**
    -   [ ] Ensure the link `http://localhost:8000/docs` (or the correct deployed backend docs URL) is accurate and mentioned.
-   [ ] **Environment Variable Setup:**
    -   [ ] Briefly mention the need for a `.env` file for API keys, and refer to `.env.example` and `SECURITY.md`.

## Environment Variable Documentation

-   [ ] **Create/Update `.env.example` (in project root, or `backend/.env.example` as per `TODO_API_INTEGRATIONS.md` - clarify location).**
    *   *`SECURITY.md` implies a root `.env.example` which is then copied to `backend/.env`. `TODO_API_INTEGRATIONS.md` suggests `backend/.env.example`. Let's assume `backend/.env.example` for now as it's backend-specific.* Reconcile this; a single root `.env.example` that `docker-compose` uses to populate `backend/.env` might be cleaner.
    *   For now, ensure `backend/.env.example` lists all required API keys:
        *   `OPENAI_API_KEY=`
        *   `ANTHROPIC_API_KEY=`
        *   `XAI_API_KEY=`
        *   `GOOGLE_API_KEY=`
        *   (Add any other env vars like `DATABASE_URL` if not hardcoded for SQLite path, or basic auth credentials if moved to env).
-   [ ] **Update `README.md` or `SECURITY.md` with clear instructions:**
    -   [ ] Document how to copy `.env.example` to `.env`.
    -   [ ] List all required environment variables and briefly explain what they are for.
    -   [ ] Reiterate that `.env` should not be committed.

## General Project Structure Documentation (Optional)

-   [ ] Consider adding a brief section to `README.md` explaining the project directory structure if it becomes complex. 