# Prompt Builder & Optimizer

A local web application for Raspberry Pi that helps users craft and optimize prompts for major language models including OpenAI, Anthropic (Claude), xAI (Grok), and Google Gemini.

## Features

- **Dynamic Prompt Collection**: Simple interface for base prompt input
- **Adaptive Questionnaire**: Context-gathering questions based on initial prompt
- **Multi-Model Support**: OpenAI, Anthropic, xAI, and Google Gemini integration
- **Side-by-Side Comparison**: Compare outputs across different models
- **Prompt Optimization**: Tailored prompts for each model's strengths
- **History & Persistence**: Local SQLite database for prompt storage

## Quick Start

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

## Tech Stack

- **Frontend**: React.js with Tailwind CSS
- **Backend**: Python FastAPI
- **Database**: SQLite
- **Deployment**: Docker on Raspberry Pi

## Development

This is a single-user application designed for local network use on Raspberry Pi. See GUIDELINES.md for complete project specifications.

## API Documentation

Backend API available at: http://localhost:8000/docs