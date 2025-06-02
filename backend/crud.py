from sqlmodel import Session, select
from typing import List, Optional

import models
import schemas

# User CRUD operations
def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    db_user = models.User.model_validate(user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int) -> Optional[models.User]:
    return db.get(models.User, user_id)

def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    statement = select(models.User).where(models.User.username == username)
    return db.exec(statement).first()

# Prompt CRUD operations
def create_prompt(db: Session, prompt: schemas.PromptCreate, user_id: Optional[int] = None) -> models.Prompt:
    db_prompt = models.Prompt.model_validate(prompt, update={"user_id": user_id})
    db.add(db_prompt)
    db.commit()
    db.refresh(db_prompt)
    return db_prompt

def get_prompt(db: Session, prompt_id: int) -> Optional[models.Prompt]:
    return db.get(models.Prompt, prompt_id)

def get_prompts(db: Session, skip: int = 0, limit: int = 100) -> List[models.Prompt]:
    statement = select(models.Prompt).offset(skip).limit(limit)
    return db.exec(statement).all()

def get_prompts_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[models.Prompt]:
    statement = select(models.Prompt).where(models.Prompt.user_id == user_id).offset(skip).limit(limit)
    return db.exec(statement).all()

# QuestionnaireResponse CRUD operations
def create_questionnaire_response(db: Session, response: schemas.QuestionnaireResponseCreate, prompt_id: int) -> models.QuestionnaireResponse:
    db_response = models.QuestionnaireResponse.model_validate(response, update={"prompt_id": prompt_id})
    db.add(db_response)
    db.commit()
    db.refresh(db_response)
    return db_response

def create_multiple_questionnaire_responses(db: Session, responses: List[schemas.QuestionnaireResponseCreate], prompt_id: int) -> List[models.QuestionnaireResponse]:
    db_responses = []
    for response_data in responses:
        db_response = models.QuestionnaireResponse.model_validate(response_data, update={"prompt_id": prompt_id})
        db.add(db_response)
        db_responses.append(db_response)
    db.commit()
    for db_response in db_responses:
        db.refresh(db_response)
    return db_responses

def get_questionnaire_responses_by_prompt(db: Session, prompt_id: int) -> List[models.QuestionnaireResponse]:
    statement = select(models.QuestionnaireResponse).where(models.QuestionnaireResponse.prompt_id == prompt_id)
    return db.exec(statement).all()

# ModelOutput CRUD operations
def create_model_output(db: Session, output: schemas.ModelOutputCreate, prompt_id: int) -> models.ModelOutput:
    db_output = models.ModelOutput.model_validate(output, update={"prompt_id": prompt_id})
    db.add(db_output)
    db.commit()
    db.refresh(db_output)
    return db_output

def get_model_outputs_by_prompt(db: Session, prompt_id: int) -> List[models.ModelOutput]:
    statement = select(models.ModelOutput).where(models.ModelOutput.prompt_id == prompt_id)
    return db.exec(statement).all()
