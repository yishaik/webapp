from fastapi import FastAPI, Depends, HTTPException, APIRouter
from typing import List, Optional

from sqlmodel import Session
from fastapi.middleware.cors import CORSMiddleware

from backend import crud, models, schemas
from backend.database import get_session, create_db_and_tables # SQLModel setup

# Create FastAPI app
app = FastAPI(title="Prompt Interaction History API", version="1.0.0")

# Add CORS middleware (important for frontend integration)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows all origins for simplicity, adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
history_router = APIRouter(prefix="/history", tags=["History"])
interaction_router = APIRouter(tags=["Interactions"])

@app.on_event("startup")
def on_startup():
    create_db_and_tables() # Creates tables based on SQLModel definitions

# History Endpoints
@history_router.get("/prompts", response_model=List[schemas.PromptRead])
def list_all_prompts(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_session)
):
    prompts = crud.get_all_prompts(db=db, skip=skip, limit=limit)
    return prompts

@history_router.get("/prompt/{prompt_id}", response_model=schemas.PromptRead)
def get_full_prompt_details(prompt_id: int, db: Session = Depends(get_session)):
    db_prompt = crud.get_prompt(db=db, prompt_id=prompt_id)
    if db_prompt is None:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return db_prompt

# Interaction Endpoints
@interaction_router.post("/questionnaires/submit", response_model=schemas.PromptRead)
def submit_questionnaire_and_create_prompt(
    request_data: schemas.SubmitQuestionnaireRequest, db: Session = Depends(get_session)
):
    prompt_create_data = schemas.PromptCreate(
        base_prompt=request_data.base_prompt,
        user_id=request_data.user_id
    )
    created_prompt = crud.create_prompt(db=db, prompt_in=prompt_create_data)

    qr_create_list: List[schemas.QuestionnaireResponseCreate] = []
    for resp_data in request_data.responses:
        qr_create_list.append(schemas.QuestionnaireResponseCreate(
            question=resp_data.question,
            answer=resp_data.answer,
            prompt_id=created_prompt.id
        ))

    # The prompt_id_override in create_multiple_questionnaire_responses ensures all responses
    # are linked to the created_prompt.id, even if individual items in qr_create_list had a (wrong) one.
    crud.create_multiple_questionnaire_responses(
        db=db, responses_in=qr_create_list, prompt_id_override=created_prompt.id
    )

    db.refresh(created_prompt)
    # At this point, created_prompt.questionnaire_responses should be populated
    # if the relationship in models.Prompt is correctly set up and the session is active.
    # Pydantic's from_attributes=True in PromptRead will handle serialization.
    return created_prompt

@interaction_router.post("/prompts/{prompt_id}/model_outputs", response_model=schemas.ModelOutputRead)
def record_model_output_for_prompt(
    prompt_id: int,
    output_data: schemas.ModelOutputCreateNoPromptId,
    db: Session = Depends(get_session)
):
    db_prompt = crud.get_prompt(db=db, prompt_id=prompt_id)
    if db_prompt is None:
        raise HTTPException(status_code=404, detail="Prompt not found, cannot record model output.")

    model_output_create_data = schemas.ModelOutputCreate(
        model_name=output_data.model_name,
        output=output_data.output,
        prompt_id=prompt_id
    )
    created_output = crud.create_model_output(db=db, output_in=model_output_create_data)
    return created_output

# Include routers
app.include_router(history_router)
app.include_router(interaction_router)

@app.get("/")
async def root():
    return {"message": "Prompt Interaction History API is running. See /docs for API documentation."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True) # Added reload for development