from fastapi import FastAPI, Depends, HTTPException # Depends and HTTPException will be used later
from fastapi.middleware.cors import CORSMiddleware
# from sqlalchemy.orm import Session # Replaced by SQLModel Session
import uvicorn
from typing import List # For list response models

# Updated imports for SQLModel
from .database import get_session, create_db_and_tables
from . import schemas # Import schemas module
from . import crud # Import crud module
# from . import models # models are used via crud and schemas
from sqlmodel import Session # For Depends

app = FastAPI(title="Prompt Builder API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], # Adjust as necessary for your frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
async def root():
    return {"message": "Prompt Builder API is running"}

@app.get("/health")
async def health_check():
    # Basic health check. Can be expanded to check DB connection later.
    return {"status": "healthy"}

# --- History Endpoints ---

from .security import verify_credentials # Import the basic auth dependency

# ... (other imports)

# --- History Endpoints ---

@app.get("/history/prompts", response_model=List[schemas.PromptRead])
async def list_all_prompts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_session),
    current_user: str = Depends(verify_credentials) # Protect endpoint
):
    prompts = crud.get_prompts(db=db, skip=skip, limit=limit)
    return prompts

@app.get("/history/prompt/{prompt_id}", response_model=schemas.PromptReadWithDetails)
async def get_prompt_details(
    prompt_id: int,
    db: Session = Depends(get_session),
    current_user: str = Depends(verify_credentials) # Protect endpoint
):
    db_prompt = crud.get_prompt(db=db, prompt_id=prompt_id)
    if db_prompt is None:
        raise HTTPException(status_code=404, detail="Prompt not found")

    # The db_prompt is a models.Prompt object.
    # Pydantic/SQLModel will automatically serialize it using PromptReadWithDetails.
    # This includes fetching the related questionnaire_responses and model_outputs
    # because they are defined as relationships in models.Prompt and included in schemas.PromptReadWithDetails.
    return db_prompt

# --- Questionnaire Generation Endpoint ---
from .questionnaire import generate_questions # Import questionnaire generation logic

@app.post("/generate_questionnaire", response_model=schemas.GeneratedQuestionnaire)
async def generate_questionnaire_endpoint(
    request: schemas.InitialPromptRequest,
    current_user: str = Depends(verify_credentials) # Protect endpoint
):
    questions = generate_questions(request.base_prompt)
    return schemas.GeneratedQuestionnaire(questions=questions)

# --- Questionnaire Submission Endpoint ---
@app.post("/submit_questionnaire", response_model=schemas.PromptReadWithDetails)
async def submit_questionnaire_endpoint(
    request: schemas.SubmitQuestionnaireRequest,
    db: Session = Depends(get_session),
    current_user: str = Depends(verify_credentials) # Protect endpoint
):
    # Create the Prompt entry
    # For now, user_id is not linked to the basic auth user.
    # If we wanted to link, we'd need to fetch/create a User from current_user (username)
    prompt_create_schema = schemas.PromptCreate(base_prompt=request.base_prompt)
    created_prompt = crud.create_prompt(db=db, prompt=prompt_create_schema, user_id=None)

    # Create the associated QuestionnaireResponse entries
    if request.responses:
        crud.create_multiple_questionnaire_responses(
            db=db, responses=request.responses, prompt_id=created_prompt.id
        )

    # Fetch the prompt with its details to return
    # The crud.get_prompt function should ideally fetch relationships if the schema expects them.
    # SQLModel handles this when Pydantic serializes the response.
    # Re-fetch the prompt to ensure all relationships are loaded for the response model
    detailed_prompt = crud.get_prompt(db=db, prompt_id=created_prompt.id)
    if detailed_prompt is None:
        raise HTTPException(status_code=500, detail="Failed to create or retrieve prompt after submission")

    return detailed_prompt

# --- Prompt Optimization Endpoint ---
from .prompt_optimizer import optimize_prompt # Import prompt optimization logic

@app.post("/optimize_prompt", response_model=schemas.OptimizedPromptResponse)
async def optimize_prompt_endpoint(
    request: schemas.OptimizePromptRequest,
    db: Session = Depends(get_session),
    current_user: str = Depends(verify_credentials) # Protect endpoint
):
    # Fetch the base prompt
    prompt_obj = crud.get_prompt(db=db, prompt_id=request.prompt_id)
    if not prompt_obj:
        raise HTTPException(status_code=404, detail="Prompt not found")

    # Fetch questionnaire answers
    # The prompt_obj from crud.get_prompt should have relationships loaded if accessed.
    # SQLModel/Pydantic handles the serialization of these nested objects.
    # We need to ensure that when crud.get_prompt is called, the session remains active
    # or that relationships are explicitly loaded if needed by optimize_prompt.
    # For SQLModel, accessing prompt_obj.questionnaire_responses should lazy-load if session is active,
    # or they should be available if .all() was used on a query with relationships.
    # The current crud.get_prompt uses db.get(), which might require explicit loading for relationships
    # if they are to be passed to another function. However, Pydantic serialization for response_model
    # usually handles this. Let's test. If not, will adjust crud.get_prompt.

    # The `optimize_prompt` function expects a list of `schemas.QuestionnaireResponseRead`.
    # The `prompt_obj.questionnaire_responses` will be a list of `models.QuestionnaireResponse`.
    # We need to convert them.

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
from .model_recommender import recommend_models # Import model recommendation logic

@app.post("/recommend_models", response_model=schemas.RecommendedModelsResponse)
async def recommend_models_endpoint(
    request: schemas.RecommendModelsRequest,
    db: Session = Depends(get_session),
    current_user: str = Depends(verify_credentials) # Protect endpoint
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

# --- Unified Model Response Endpoint ---
# Import API handlers
from .api_handlers import openai_handler, claude_handler, grok_handler, gemini_handler
from .prompt_optimizer import optimize_prompt # Re-using the optimization logic

# Model mapping: Friendly Name -> (Actual SDK Model Name, Handler Module, Max Output Tokens (optional, for reference))
# Max output tokens are from the respective *_API_INSTRUCTIONS.md
MODEL_MAP = {
    # OpenAI
    "GPT-4.1": ("gpt-4o", openai_handler, 8192), # Assuming GPT-4.1 maps to gpt-4o
    "GPT-4.1 Mini": ("gpt-4-turbo", openai_handler, 8192), # Assuming Mini maps to gpt-4-turbo
    "GPT-4.1 Nano": ("gpt-3.5-turbo", openai_handler, 4096), # Assuming Nano maps to gpt-3.5-turbo (adjust if needed)
    # Anthropic
    "Claude Opus 4": ("claude-3-opus-20240229", claude_handler, 4096),
    "Claude Sonnet 4": ("claude-3-sonnet-20240229", claude_handler, 4096),
    # xAI
    "Grok-3": ("grok-3", grok_handler, 8192),
    "Grok-3 Mini": ("grok-3-mini", grok_handler, 8192),
    # Google
    "Gemini 2.5 Pro": ("gemini-1.5-pro-latest", gemini_handler, 8192), # Gemini has large context, output tokens can be high
    "Gemini 2.5 Flash": ("gemini-1.5-flash-latest", gemini_handler, 8192),
}


@app.post("/get_model_response", response_model=schemas.ModelResponseResponse)
async def get_model_response_endpoint(
    request: schemas.ModelResponseRequest,
    db: Session = Depends(get_session),
    current_user: str = Depends(verify_credentials) # Protect endpoint
):
    # 1. Fetch the Prompt object
    prompt_obj = crud.get_prompt(db=db, prompt_id=request.prompt_id)
    if not prompt_obj:
        raise HTTPException(status_code=404, detail=f"Prompt with ID {request.prompt_id} not found.")

    # 2. Get an optimized prompt
    # Convert model.QuestionnaireResponse to schema.QuestionnaireResponseRead for the optimizer
    questionnaire_responses_read: List[schemas.QuestionnaireResponseRead] = []
    if prompt_obj.questionnaire_responses:
        for qr_model in prompt_obj.questionnaire_responses:
            questionnaire_responses_read.append(schemas.QuestionnaireResponseRead.model_validate(qr_model))

    # The target_model for optimization can be the friendly name for now,
    # as optimize_prompt doesn't use it for specific logic yet.
    optimized_prompt_str = optimize_prompt(
        base_prompt=prompt_obj.base_prompt,
        questionnaire_answers=questionnaire_responses_read,
        target_model=request.model_name
    )

    # 3. Determine which API handler and actual SDK model identifier to use
    if request.model_name not in MODEL_MAP:
        raise HTTPException(status_code=400, detail=f"Model '{request.model_name}' is not supported.")

    sdk_model_name, handler_module, _ = MODEL_MAP[request.model_name]

    # 4. Call the appropriate handler function
    llm_output_str = handler_module.get_llm_response(
        prompt=optimized_prompt_str,
        model_name=sdk_model_name
    )

    # Check for errors from the handler (convention: starts with "Error:")
    if llm_output_str.startswith("Error:"):
        # Log the full error from handler for backend visibility
        logging.error(f"LLM handler for model {sdk_model_name} returned an error for prompt ID {request.prompt_id}: {llm_output_str}")
        # Return a more generic error to the client, or the specific one if desired
        raise HTTPException(status_code=502, detail=f"LLM API call failed: {llm_output_str}")

    # 5. Store the LLM's output
    model_output_create = schemas.ModelOutputCreate(
        model_name=request.model_name, # Store the friendly name
        output=llm_output_str
    )
    crud.create_model_output(db=db, output=model_output_create, prompt_id=request.prompt_id)

    # 6. Return the model's response
    return schemas.ModelResponseResponse(
        prompt_id=request.prompt_id,
        model_name=request.model_name,
        output=llm_output_str,
        optimized_prompt_used=optimized_prompt_str
    )

# Commenting out old endpoints, will be replaced by history endpoints
# @app.post("/prompts/", response_model=schemas.PromptRead) # Updated response_model
# async def create_prompt_endpoint(prompt: schemas.PromptCreate, db: Session = Depends(get_session)):
#     # This is a placeholder, actual prompt creation might involve user association etc.
#     # The task specifies /submit_questionnaire for creating Prompt and QuestionnaireResponses
#     # and /get_model_response for ModelOutputs.
#     # This old endpoint might not directly map to the new requirements.
#     # return crud.create_prompt(db=db, prompt=prompt) # Example if we had a simple prompt creation
#     raise HTTPException(status_code=501, detail="Not implemented")


# @app.get("/prompts/", response_model=List[schemas.PromptRead]) # Updated response_model
# async def get_prompts_endpoint(db: Session = Depends(get_session)):
#     # This is a placeholder, actual prompt listing is specified as /history/prompts
#     # return crud.get_prompts(db=db)
#     raise HTTPException(status_code=501, detail="Not implemented")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) # Added reload for dev