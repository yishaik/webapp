from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
import secrets
import os
from dotenv import load_dotenv
from typing import List # Added for type hinting
import uvicorn

from database import get_db, create_tables
from models import *
from questionnaire import generate_questions # Added import
from prompt_optimizer import optimize_prompt # Added import
from model_recommender import recommend_models # Added import

# Simple model for submitting questionnaire answers
class QuestionnaireSubmission(BaseModel):
    prompt: str
    answers: List[str]

# Model for the prompt optimization request
class OptimizePromptRequest(BaseModel):
    initial_prompt: str
    questionnaire_answers: List[str]
    target_model: str

# Model for the model recommendation request
class RecommendModelsRequest(BaseModel):
    initial_prompt: str
    questionnaire_answers: List[str]

# In-memory storage for questionnaire submissions (temporary)
questionnaire_submissions_db = []

app = FastAPI(title="Prompt Builder API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load environment variables from .env file
load_dotenv()

# Basic Authentication
security = HTTPBasic()

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, os.environ.get("BASIC_AUTH_USERNAME"))
    correct_password = secrets.compare_digest(credentials.password, os.environ.get("BASIC_AUTH_PASSWORD"))
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# Apply basic authentication to all routes
app.dependency_overrides[get_current_username] = get_current_username

# Create database tables on startup
create_tables()

@app.get("/")
async def root(username: str = Depends(get_current_username)):
    return {"message": "Prompt Builder API is running"}

@app.get("/health")
async def health_check(username: str = Depends(get_current_username)):
    return {"status": "healthy"}

@app.post("/prompts/", response_model=Prompt)
async def create_prompt(prompt: PromptCreate, db: Session = Depends(get_db), username: str = Depends(get_current_username)):
    from database import Prompt as DBPrompt
    db_prompt = DBPrompt(**prompt.dict())
    db.add(db_prompt)
    db.commit()
    db.refresh(db_prompt)
    return db_prompt

@app.get("/prompts/", response_model=List[Prompt])
async def get_prompts(db: Session = Depends(get_db), username: str = Depends(get_current_username)):
    from database import Prompt as DBPrompt
    return db.query(DBPrompt).all()

@app.post("/generate_questionnaire")
async def post_generate_questionnaire(request_data: PromptBase, username: str = Depends(get_current_username)):
    questions = generate_questions(request_data.base_prompt)
    return {"questions": questions}

@app.post("/submit_questionnaire")
async def post_submit_questionnaire(submission: QuestionnaireSubmission, username: str = Depends(get_current_username)):
    # Store in-memory (for now)
    questionnaire_submissions_db.append({"prompt": submission.prompt, "answers": submission.answers})
    return {"message": "Questionnaire submitted successfully.", "submission_id": len(questionnaire_submissions_db)}

@app.post("/optimize_prompt")
async def post_optimize_prompt(request_data: OptimizePromptRequest, username: str = Depends(get_current_username)):
    optimized_prompt_text = optimize_prompt(
        initial_prompt=request_data.initial_prompt,
        questionnaire_answers=request_data.questionnaire_answers,
        target_model=request_data.target_model
    )
    return {"optimized_prompt": optimized_prompt_text}

@app.post("/recommend_models")
async def post_recommend_models(request_data: RecommendModelsRequest, username: str = Depends(get_current_username)):
    recommended_model_ids = recommend_models(
        initial_prompt=request_data.initial_prompt,
        questionnaire_answers=request_data.questionnaire_answers
    )
    return {"recommended_models": recommended_model_ids}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)