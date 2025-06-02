from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
import secrets
import os
from dotenv import load_dotenv
from typing import List
import uvicorn

from database import get_db, create_tables
from models import *
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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Basic Authentication
security = HTTPBasic()

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, os.environ.get("BASIC_AUTH_USERNAME", "admin"))
    correct_password = secrets.compare_digest(credentials.password, os.environ.get("BASIC_AUTH_PASSWORD", "password"))
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# In-memory storage for questionnaire submissions (temporary)
questionnaire_submissions_db = []

@app.on_event("startup")
def startup_event():
    create_tables()

@app.get("/")
async def root():
    return {"message": "Prompt Builder and Optimizer API is running"}

@app.post("/create_prompt/", response_model=PromptResponse)
async def create_prompt(prompt: PromptCreate, db: Session = Depends(get_db), username: str = Depends(get_current_username)):
    from database import Prompt as DBPrompt
    db_prompt = DBPrompt(base_prompt=prompt.base_prompt, user_id=prompt.user_id)
    db.add(db_prompt)
    db.commit()
    db.refresh(db_prompt)
    return db_prompt

@app.get("/prompts/", response_model=List[PromptResponse])
async def get_prompts(db: Session = Depends(get_db), username: str = Depends(get_current_username)):
    from database import Prompt as DBPrompt
    return db.query(DBPrompt).all()

@app.post("/generate_questionnaire")
async def post_generate_questionnaire(request_data: PromptBase, username: str = Depends(get_current_username)):
    questions = generate_questions(request_data.base_prompt)
    return {"questions": questions}

@app.post("/submit_questionnaire")
async def post_submit_questionnaire(submission: QuestionnaireSubmission, username: str = Depends(get_current_username)):
    questionnaire_submissions_db.append(submission.dict())
    return {"status": "success", "message": "Questionnaire submitted successfully"}

@app.post("/optimize_prompt")
async def post_optimize_prompt(request_data: PromptBase, username: str = Depends(get_current_username)):
    optimized = optimize_prompt(request_data.base_prompt)
    return {"optimized_prompt": optimized}

@app.post("/recommend_models")
async def post_recommend_models(request_data: RecommendModelsRequest, username: str = Depends(get_current_username)):
    recommended_model_ids = recommend_models(
        initial_prompt=request_data.initial_prompt,
        questionnaire_answers=request_data.questionnaire_answers
    )
    return {"recommended_models": recommended_model_ids}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)