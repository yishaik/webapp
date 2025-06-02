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
from database import get_db, create_db_and_tables
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

@app.get("/secure-data")
async def get_secure_data(username: str = Depends(verify_credentials)):
    return {"message": f"Hello {username}, you have accessed secure data!"}

# --- History Endpoints ---

@app.get("/history/prompts", response_model=List[schemas.PromptRead])
async def list_all_prompts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: str = Depends(verify_credentials)  # Protect endpoint
):
    prompts = crud.get_prompts(db=db, skip=skip, limit=limit)
    return prompts

@app.get("/history/prompt/{prompt_id}", response_model=schemas.PromptReadWithDetails)
async def get_prompt_details(
    prompt_id: int,
    db: Session = Depends(get_db),
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
    db: Session = Depends(get_db),
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
    request: schemas.OptimizePromptRequest, # Updated schema
    current_user: str = Depends(verify_credentials)  # Protect endpoint
    # db: Session = Depends(get_db) # No longer needed for this direct version
):
    # Ensure questionnaire_responses is not None, default to empty list if so
    # The optimize_prompt function now expects List[QuestionnaireResponseCreate] or None
    questionnaire_responses_for_optimizer = request.questionnaire_responses if request.questionnaire_responses is not None else []

    optimized_text = optimize_prompt(
        base_prompt=request.base_prompt,
        questionnaire_answers=questionnaire_responses_for_optimizer,
        target_model=request.target_model
    )
    return schemas.OptimizedPromptResponse(optimized_prompt=optimized_text)

# --- Model Recommendation Endpoint ---

@app.post("/recommend_models", response_model=schemas.RecommendedModelsResponse)
async def recommend_models_endpoint(
    request: schemas.ModelRecommendationDirectRequest, # Changed request schema
    current_user: str = Depends(verify_credentials)  # Protect endpoint
    # db: Session = Depends(get_db) # Not needed if not fetching prompt_id
):
    # Ensure questionnaire_responses is not None, default to empty list if so
    questionnaire_responses_for_recommender = request.questionnaire_responses if request.questionnaire_responses is not None else []

    recommended_model_names = recommend_models(
        base_prompt=request.base_prompt,
        questionnaire_answers=questionnaire_responses_for_recommender
    )
    return schemas.RecommendedModelsResponse(models=recommended_model_names)

# --- Basic CRUD Endpoints (for compatibility) ---

@app.post("/create_prompt/", response_model=schemas.PromptRead)
async def create_prompt(
    prompt: schemas.PromptCreate, 
    db: Session = Depends(get_db),
    current_user: str = Depends(verify_credentials)
):
    return crud.create_prompt(db=db, prompt=prompt, user_id=None)

@app.get("/prompts/", response_model=List[schemas.PromptRead])
async def get_prompts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: str = Depends(verify_credentials)
):
    return crud.get_prompts(db=db, skip=skip, limit=limit)

# --- Advanced Model Response Endpoint ---
from backend.api_handlers import openai_handler, claude_handler, grok_handler, gemini_handler

# Model mapping for advanced endpoint
# Maps user-friendly names to (actual_model_name_for_api, handler_module, context_window_size_optional)
MODEL_MAP = {
    "GPT-4.1": ("gpt-4o", openai_handler, 8192), # Assuming gpt-4o is the latest "GPT-4.1"
    "GPT-4.1 Mini": ("gpt-4-turbo", openai_handler, 8192), # Or another suitable smaller model
    "GPT-4.1 Nano": ("gpt-3.5-turbo", openai_handler, 4096),
    "Claude Opus 4": ("claude-3-opus-20240229", claude_handler, 4096), # Max output tokens, not context window from docs
    "Claude Sonnet 4": ("claude-3-sonnet-20240229", claude_handler, 4096),
    "Grok-3": ("grok-3", grok_handler, 8192),
    "Grok-3 Mini": ("grok-3-mini", grok_handler, 8192),
    "Gemini 2.5 Pro": ("gemini-1.5-pro-latest", gemini_handler, 8192), # Context window not specified, using common large value
    "Gemini 2.5 Flash": ("gemini-1.5-flash-latest", gemini_handler, 8192),
}

@app.post("/get_model_response", response_model=schemas.ModelInteractionResponse)
async def get_model_response_endpoint(
    request: schemas.ModelInteractionRequest,
    db: Session = Depends(get_db),
    current_user: str = Depends(verify_credentials)
):
    final_prompt_text: str = ""
    prompt_id_to_log: Optional[int] = request.prompt_id
    actual_prompt_for_llm: str = ""

    if request.optimized_prompt_override:
        actual_prompt_for_llm = request.optimized_prompt_override
    elif request.prompt_id:
        prompt_obj = crud.get_prompt(db, prompt_id=request.prompt_id)
        if not prompt_obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prompt not found")
        
        questionnaire_responses_for_optimizer: List[schemas.QuestionnaireResponseCreate] = []
        if prompt_obj.questionnaire_responses:
            for qr_model in prompt_obj.questionnaire_responses:
                questionnaire_responses_for_optimizer.append(
                    schemas.QuestionnaireResponseCreate.model_validate(qr_model)
                )

        actual_prompt_for_llm = optimize_prompt(
            base_prompt=prompt_obj.base_prompt,
            questionnaire_answers=questionnaire_responses_for_optimizer,
            target_model=request.model_name # Pass model_name for potential model-specific optimization
        )
    elif request.base_prompt:
        # Ensure questionnaire_responses is not None if base_prompt is used without prompt_id
        q_responses = request.questionnaire_responses if request.questionnaire_responses is not None else []
        actual_prompt_for_llm = optimize_prompt(
            base_prompt=request.base_prompt,
            questionnaire_answers=q_responses,
            target_model=request.model_name
        )
        # If base_prompt is provided, create a new Prompt entry to get an ID for logging outputs
        # This part is crucial for associating the output with a prompt.
        if not prompt_id_to_log: # Only create if no prompt_id was given initially
            new_prompt_schema = schemas.PromptCreate(base_prompt=request.base_prompt)
            created_prompt_obj = crud.create_prompt(db=db, prompt=new_prompt_schema, user_id=None) # Assuming no user for now
            prompt_id_to_log = created_prompt_obj.id
            if q_responses: # If questionnaire responses were provided with base_prompt
                crud.create_multiple_questionnaire_responses(db=db, responses=q_responses, prompt_id=prompt_id_to_log)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Either prompt_id, base_prompt, or optimized_prompt_override must be provided.")

    if not actual_prompt_for_llm:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to determine final prompt.")

    # Route to the correct LLM API handler
    if request.model_name not in MODEL_MAP:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Model '{request.model_name}' is not supported.")

    actual_model_api_name, handler_module, _ = MODEL_MAP[request.model_name]

    llm_output_text = handler_module.get_llm_response(
        prompt=actual_prompt_for_llm,
        model_name=actual_model_api_name
    )

    # Store the model output if a prompt_id is available
    if prompt_id_to_log:
        model_output_schema = schemas.ModelOutputCreate(
            model_name=request.model_name, # Log user-friendly name
            output=llm_output_text
        )
        crud.create_model_output(db=db, output=model_output_schema, prompt_id=prompt_id_to_log)

    return schemas.ModelInteractionResponse(
        model_name=request.model_name,
        output=llm_output_text,
        prompt_id=prompt_id_to_log,
        optimized_prompt_used=actual_prompt_for_llm if actual_prompt_for_llm != request.base_prompt else None
    )

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
