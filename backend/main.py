from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import List
import os
import secrets
import logging
from dotenv import load_dotenv

# SQLModel imports (using modern approach from HEAD)
from sqlmodel import Session
from database import get_session, create_db_and_tables
import schemas
import crud
from security import verify_credentials
from questionnaire import generate_questions
from prompt_optimizer import optimize_prompt
from model_recommender import recommend_models

# Load environment variables from .env file
load_dotenv()

# Create FastAPI app
app = FastAPI(title="Prompt Builder and Optimizer API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Secure default for local development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    create_db_and_tables()

@app.get("/")
async def root():
    return {"message": "Prompt Builder and Optimizer API is running"}

@app.get("/health")
async def health_check():
    # Basic health check. Can be expanded to check DB connection later.
    return {"status": "healthy"}

# --- History Endpoints ---

@app.get("/history/prompts", response_model=List[schemas.PromptRead])
async def list_all_prompts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_session),
    current_user: str = Depends(verify_credentials)  # Protect endpoint
):
    prompts = crud.get_prompts(db=db, skip=skip, limit=limit)
    return prompts

@app.get("/history/prompt/{prompt_id}", response_model=schemas.PromptReadWithDetails)
async def get_prompt_details(
    prompt_id: int,
    db: Session = Depends(get_session),
    current_user: str = Depends(verify_credentials)  # Protect endpoint
):
    db_prompt = crud.get_prompt(db=db, prompt_id=prompt_id)
    if db_prompt is None:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return db_prompt

# --- Questionnaire Generation Endpoint ---

@app.post("/generate_questionnaire", response_model=schemas.GeneratedQuestionnaire)
async def generate_questionnaire_endpoint(
    request: schemas.InitialPromptRequest,
    current_user: str = Depends(verify_credentials)  # Protect endpoint
):
    questions = generate_questions(request.base_prompt)
    return schemas.GeneratedQuestionnaire(questions=questions)

# --- Questionnaire Submission Endpoint ---
@app.post("/submit_questionnaire", response_model=schemas.PromptReadWithDetails)
async def submit_questionnaire_endpoint(
    request: schemas.SubmitQuestionnaireRequest,
    db: Session = Depends(get_session),
    current_user: str = Depends(verify_credentials)  # Protect endpoint
):
    # Create the Prompt entry
    prompt_create_schema = schemas.PromptCreate(base_prompt=request.base_prompt)
    created_prompt = crud.create_prompt(db=db, prompt=prompt_create_schema, user_id=None)

    # Create the associated QuestionnaireResponse entries
    if request.responses:
        crud.create_multiple_questionnaire_responses(
            db=db, responses=request.responses, prompt_id=created_prompt.id
        )

    # Fetch the prompt with its details to return
    detailed_prompt = crud.get_prompt(db=db, prompt_id=created_prompt.id)
    if detailed_prompt is None:
        raise HTTPException(status_code=500, detail="Failed to create or retrieve prompt after submission")

    return detailed_prompt

# --- Prompt Optimization Endpoint ---

@app.post("/optimize_prompt", response_model=schemas.OptimizedPromptResponse)
async def optimize_prompt_endpoint(
    request: schemas.OptimizePromptRequest,
    db: Session = Depends(get_session),
    current_user: str = Depends(verify_credentials)  # Protect endpoint
):
    # Fetch the base prompt
    prompt_obj = crud.get_prompt(db=db, prompt_id=request.prompt_id)
    if not prompt_obj:
        raise HTTPException(status_code=404, detail="Prompt not found")

    # Convert model.QuestionnaireResponse to schema.QuestionnaireResponseRead
    questionnaire_responses_read: List[schemas.QuestionnaireResponseRead] = []
    if prompt_obj.questionnaire_responses:
        for qr_model in prompt_obj.questionnaire_responses:
            questionnaire_responses_read.append(schemas.QuestionnaireResponseRead.model_validate(qr_model))

    optimized_text = optimize_prompt(
        base_prompt=prompt_obj.base_prompt,
        questionnaire_answers=questionnaire_responses_read,
        target_model=request.target_model
    )
    return schemas.OptimizedPromptResponse(optimized_prompt=optimized_text)

# --- Model Recommendation Endpoint ---

@app.post("/recommend_models", response_model=schemas.RecommendedModelsResponse)
async def recommend_models_endpoint(
    request: schemas.RecommendModelsRequest,
    db: Session = Depends(get_session),
    current_user: str = Depends(verify_credentials)  # Protect endpoint
):
    prompt_obj = crud.get_prompt(db=db, prompt_id=request.prompt_id)
    if not prompt_obj:
        raise HTTPException(status_code=404, detail="Prompt not found")

    # Convert model.QuestionnaireResponse to schema.QuestionnaireResponseRead
    questionnaire_responses_read: List[schemas.QuestionnaireResponseRead] = []
    if prompt_obj.questionnaire_responses:
        for qr_model in prompt_obj.questionnaire_responses:
            questionnaire_responses_read.append(schemas.QuestionnaireResponseRead.model_validate(qr_model))

    recommended_model_names = recommend_models(
        base_prompt=prompt_obj.base_prompt,
        questionnaire_answers=questionnaire_responses_read
    )
    return schemas.RecommendedModelsResponse(models=recommended_model_names)

# --- Basic CRUD Endpoints (for compatibility) ---

@app.post("/create_prompt/", response_model=schemas.PromptRead)
async def create_prompt(
    prompt: schemas.PromptCreate, 
    db: Session = Depends(get_session), 
    current_user: str = Depends(verify_credentials)
):
    return crud.create_prompt(db=db, prompt=prompt, user_id=None)

@app.get("/prompts/", response_model=List[schemas.PromptRead])
async def get_prompts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_session), 
    current_user: str = Depends(verify_credentials)
):
    return crud.get_prompts(db=db, skip=skip, limit=limit)

# --- Advanced Model Response Endpoint (when API handlers are available) ---
# Uncomment when api_handlers module is implemented
"""
try:
    from api_handlers import openai_handler, claude_handler, grok_handler, gemini_handler
    
    # Model mapping for advanced endpoint
    MODEL_MAP = {
        "GPT-4.1": ("gpt-4o", openai_handler, 8192),
        "GPT-4.1 Mini": ("gpt-4-turbo", openai_handler, 8192),
        "GPT-4.1 Nano": ("gpt-3.5-turbo", openai_handler, 4096),
        "Claude Opus 4": ("claude-3-opus-20240229", claude_handler, 4096),
        "Claude Sonnet 4": ("claude-3-sonnet-20240229", claude_handler, 4096),
        "Grok-3": ("grok-3", grok_handler, 8192),
        "Grok-3 Mini": ("grok-3-mini", grok_handler, 8192),
        "Gemini 2.5 Pro": ("gemini-1.5-pro-latest", gemini_handler, 8192),
        "Gemini 2.5 Flash": ("gemini-1.5-flash-latest", gemini_handler, 8192),
    }

    @app.post("/get_model_response", response_model=schemas.ModelResponseResponse)
    async def get_model_response_endpoint(
        request: schemas.ModelResponseRequest,
        db: Session = Depends(get_session),
        current_user: str = Depends(verify_credentials)
    ):
        # Implementation here when handlers are available
        pass
        
except ImportError:
    # API handlers not available, endpoint will be disabled
    pass
"""

# Legacy endpoints maintained for backward compatibility
@app.post("/generate_questionnaire_legacy")
async def post_generate_questionnaire_legacy(
    request_data: schemas.InitialPromptRequest, 
    current_user: str = Depends(verify_credentials)
):
    questions = generate_questions(request_data.base_prompt)
    return {"questions": questions}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
