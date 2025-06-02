from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import uvicorn

from database import get_db, create_tables
from models import *

app = FastAPI(title="Prompt Builder API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables on startup
create_tables()

@app.get("/")
async def root():
    return {"message": "Prompt Builder API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/prompts/", response_model=Prompt)
async def create_prompt(prompt: PromptCreate, db: Session = Depends(get_db)):
    from database import Prompt as DBPrompt
    db_prompt = DBPrompt(**prompt.dict())
    db.add(db_prompt)
    db.commit()
    db.refresh(db_prompt)
    return db_prompt

@app.get("/prompts/", response_model=List[Prompt])
async def get_prompts(db: Session = Depends(get_db)):
    from database import Prompt as DBPrompt
    return db.query(DBPrompt).all()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)