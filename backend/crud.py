from typing import List, Optional

from sqlmodel import Session, select

from backend.models import User, Prompt, QuestionnaireResponse, ModelOutput
from backend.schemas import (
    UserCreate, UserUpdate,
    PromptCreate, PromptUpdate,
    QuestionnaireResponseCreate, # No QuestionnaireResponseUpdate defined in schemas as per previous step, but if needed, it would be here
    ModelOutputCreate, # No ModelOutputUpdate defined in schemas
)


# User CRUD
def create_user(db: Session, user_in: UserCreate) -> User:
    db_user = User.model_validate(user_in)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.get(User, user_id)

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    statement = select(User).where(User.username == username)
    return db.exec(statement).first()

def update_user(db: Session, user_db: User, user_in: UserUpdate) -> User:
    user_data = user_in.model_dump(exclude_unset=True)
    for key, value in user_data.items():
        setattr(user_db, key, value)
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db

def delete_user(db: Session, user_id: int) -> Optional[User]:
    db_user = db.get(User, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user


# Prompt CRUD
def create_prompt(db: Session, prompt_in: PromptCreate) -> Prompt:
    # user_id is part of PromptCreate and will be handled by model_validate
    db_prompt = Prompt.model_validate(prompt_in)
    db.add(db_prompt)
    db.commit()
    db.refresh(db_prompt)
    return db_prompt

def get_prompt(db: Session, prompt_id: int) -> Optional[Prompt]:
    # Eager loading can be added here if consistently needed, but often better at API layer
    return db.get(Prompt, prompt_id)

def get_prompts_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Prompt]:
    statement = select(Prompt).where(Prompt.user_id == user_id).offset(skip).limit(limit)
    return db.exec(statement).all()

def get_all_prompts(db: Session, skip: int = 0, limit: int = 100) -> List[Prompt]:
    statement = select(Prompt).offset(skip).limit(limit)
    return db.exec(statement).all()

def update_prompt(db: Session, prompt_db: Prompt, prompt_in: PromptUpdate) -> Prompt:
    prompt_data = prompt_in.model_dump(exclude_unset=True)
    for key, value in prompt_data.items():
        setattr(prompt_db, key, value)
    db.add(prompt_db)
    db.commit()
    db.refresh(prompt_db)
    return prompt_db

def delete_prompt(db: Session, prompt_id: int) -> Optional[Prompt]:
    db_prompt = db.get(Prompt, prompt_id)
    if db_prompt:
        db.delete(db_prompt)
        db.commit()
    return db_prompt


# QuestionnaireResponse CRUD
def create_questionnaire_response(db: Session, response_in: QuestionnaireResponseCreate) -> QuestionnaireResponse:
    # prompt_id is part of QuestionnaireResponseCreate
    db_response = QuestionnaireResponse.model_validate(response_in)
    db.add(db_response)
    db.commit()
    db.refresh(db_response)
    return db_response

def create_multiple_questionnaire_responses(
    db: Session, responses_in: List[QuestionnaireResponseCreate], prompt_id_override: int
) -> List[QuestionnaireResponse]:
    db_responses = []
    for response_in in responses_in:
        # Ensure the response is associated with the provided prompt_id_override
        # even if response_in.prompt_id might be different or not set.
        # However, QuestionnaireResponseCreate requires prompt_id.
        # So, we should ensure response_in.prompt_id matches prompt_id_override or handle discrepancy.
        # For this implementation, we assume response_in.prompt_id is correctly set by the caller
        # or that prompt_id_override is the authoritative one.
        # If prompt_id is part of response_in and should be used, the override is not needed.
        # Given the spec, prompt_id_override is the authority.

        # Create a dictionary from the input schema and override/set the prompt_id
        response_data = response_in.model_dump()
        response_data['prompt_id'] = prompt_id_override # Set/Override prompt_id

        db_response = QuestionnaireResponse.model_validate(response_data)
        db.add(db_response)
        db_responses.append(db_response)

    if db_responses: # Only commit if there are responses to add
        db.commit()
        for db_response in db_responses: # Refresh each object
            db.refresh(db_response)

    return db_responses

def get_questionnaire_responses_by_prompt(db: Session, prompt_id: int) -> List[QuestionnaireResponse]:
    statement = select(QuestionnaireResponse).where(QuestionnaireResponse.prompt_id == prompt_id)
    return db.exec(statement).all()


# ModelOutput CRUD
def create_model_output(db: Session, output_in: ModelOutputCreate) -> ModelOutput:
    # prompt_id is part of ModelOutputCreate
    db_output = ModelOutput.model_validate(output_in)
    db.add(db_output)
    db.commit()
    db.refresh(db_output)
    return db_output

def get_model_outputs_by_prompt(db: Session, prompt_id: int) -> List[ModelOutput]:
    statement = select(ModelOutput).where(ModelOutput.prompt_id == prompt_id)
    return db.exec(statement).all()
