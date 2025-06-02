# Deployment TODO

This file outlines tasks for containerizing and deploying the Prompt Builder & Optimizer application on a Raspberry Pi using Docker.

## Backend Dockerization

-   [ ] **Create `backend/Dockerfile`**
    -   [ ] Use an official Python base image suitable for Raspberry Pi (e.g., `python:3.X-slim-bullseye` if ARM compatible, or look for ARM-specific Python images like `arm32v7/python` or `arm64v8/python`).
    -   [ ] Set up a working directory (e.g., `/app`).
    -   [ ] Copy `requirements.txt` and install dependencies using `pip install --no-cache-dir -r requirements.txt`.
    -   [ ] Copy the rest of the backend application code into the image.
    -   [ ] Expose the port FastAPI will run on (e.g., 8000).
    -   [ ] Define the command to run the FastAPI application (e.g., `CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]`).
-   [ ] **Create `backend/.dockerignore`**
    -   [ ] Add `venv/`, `__pycache__/`, `*.pyc`, `*.db`, `.env` and other unnecessary files/directories to prevent them from being copied into the Docker image.

## Frontend Dockerization

-   [ ] **Create `frontend/Dockerfile`**
    -   [ ] Use a multi-stage build approach.
    -   **Build Stage:**
        *   Use an official Node.js base image (e.g., `node:18-alpine` or an ARM-compatible version) as `builder`.
        *   Set working directory (e.g., `/app`).
        *   Copy `package.json` and `package-lock.json` (or `yarn.lock`).
        *   Install dependencies (`npm install` or `yarn install`).
        *   Copy the rest of the frontend application code.
        *   Build the React application (`npm run build` or `yarn build`).
    -   **Serve Stage:**
        *   Use a lightweight web server image like `nginx:alpine` (ensure ARM compatibility).
        *   Copy the built static files from the `builder` stage (e.g., from `/app/build`) into Nginx's HTML directory (e.g., `/usr/share/nginx/html`).
        *   (Optional) Add a simple Nginx configuration file (`frontend/nginx.conf`) if needed to handle routing for SPAs (e.g., redirect all to `index.html`) and copy it into the image.
        *   Expose port 80 (or other port Nginx will serve on).
-   [ ] **Create `frontend/.dockerignore`**
    -   [ ] Add `node_modules/`, `build/`, `.env`, and other unnecessary files/directories.

## Docker Compose (`docker-compose.yml`)

-   [ ] **Create `docker-compose.yml` in the project root.**
-   [ ] Define services:
    -   **`backend` service:**
        *   `build`: Context set to `./backend`.
        *   `ports`: Map a host port to the container port (e.g., `"8000:8000"`).
        *   `volumes`:
            *   Mount the SQLite database file (`prompts.db`) to a persistent location on the host (e.g., `./data/prompts.db:/app/prompts.db` or using a named volume) to ensure data persistence across container restarts.
            *   (Optional for development) Mount backend code for live reloading if Uvicorn is configured for it.
        *   `env_file`: Specify `backend/.env` to load environment variables.
        *   `restart`: `unless-stopped` or `always`.
    -   **`frontend` service:**
        *   `build`: Context set to `./frontend`.
        *   `ports`: Map a host port to the container port (e.g., `"3000:80"` if Nginx serves on 80).
        *   `depends_on`: `backend` (if frontend needs backend to be up, though often not a strict startup dependency).
        *   `restart`: `unless-stopped` or `always`.
-   [ ] (Optional) Define a top-level named `volumes` entry if using named volumes for the database.
-   [ ] Configure networking if necessary, though default bridge network is usually fine for this setup.
-   [ ] Ensure `docker-compose.yml` is configured considering Raspberry Pi's ARM architecture (base images in Dockerfiles should be ARM-compatible).

## Deployment on Raspberry Pi

-   [ ] Document steps for deploying on Raspberry Pi:
    -   Install Docker and Docker Compose on Raspberry Pi.
    -   Clone the repository.
    -   Create `backend/.env` with actual API keys on the Pi.
    -   Run `docker-compose up -d --build`.
    -   Verify application is accessible via browser on Raspberry Pi's IP address and specified port. 