# Documentation & Review TODO

This file outlines tasks for maintaining project documentation and reviewing existing guideline files.

## Review and Clarify `CLAUDE.md`

-   [ ] **Determine the purpose of `CLAUDE.md`:**
    *   Read `CLAUDE.md` and compare its content with `GUIDELINES.md`, `README.md`, and `PROJECT_TODO.md` (now split into smaller TODOs).
    *   Identify unique information in `CLAUDE.md` vs. redundant information.
    *   *Note: `CLAUDE.md` seems to be a mix of high-level overview, dev commands, and personal notes. It mentions updating itself and `README.md`.* Developer seems to be using it as a scratchpad.
-   [ ] **Integrate relevant information:**
    *   If any unique and valuable development notes or specific Claude-related API insights are found, integrate them into the appropriate new TODO files (e.g., `TODO_API_INTEGRATIONS.md` for Claude API specifics) or `README.md` if they are general setup/run commands.
    *   Development commands listed (backend, frontend, test) should be verified and added to the main `README.md` if not already present and accurate.
-   [ ] **Decision on `CLAUDE.md`:**
    *   Based on the review, decide whether to:
        *   **Remove `CLAUDE.md`**: If all its useful content is migrated and it becomes redundant.
        *   **Archive `CLAUDE.md`**: Move it to an `archive/` directory if it might have historical value but is no longer actively maintained.
        *   **Repurpose `CLAUDE.md`**: If there's a clear, specific purpose for it that doesn't overlap (e.g., very detailed notes *only* for Anthropic Claude development, unlikely given project scope).
    *   *Initial assessment suggests most of its content is covered or better placed elsewhere. Likely candidate for removal after ensuring no info is lost.*

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