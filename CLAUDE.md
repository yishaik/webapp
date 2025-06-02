# Claude Development Guide

## Project Overview
Prompt Builder and Optimizer webapp for Raspberry Pi - single user local network application that optimizes prompts for OpenAI, Anthropic, xAI, and Google Gemini models.

## Commands
- Backend: `cd backend && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt && python main.py`
- Frontend: `cd frontend && npm install && npm start`
- Test: `python -m pytest` (backend), `npm test` (frontend)

## Architecture
- Backend: Python FastAPI with SQLite database
- Frontend: React.js with Tailwind CSS
- APIs: OpenAI, Anthropic, xAI, Google Gemini integrations
- Deployment: Docker on Raspberry Pi

## Development Notes
- Always commit to GitHub with each iteration
- Update both CLAUDE.md and README.md files
- Follow guidelines in GUIDELINES.md
- Follow security guidelines in SECURITY.md
- Single user application for local network