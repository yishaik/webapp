import pytest
from sqlmodel import Session
from typing import List

from backend import crud, schemas, models

# Helper function to create a user for tests that require a user
def create_test_user(db: Session, username: str = "testuser") -> models.User:
    user_in = schemas.UserCreate(username=username, email="testuser@example.com") # email was removed from model, but schema might still have it. Let's check schemas.
    # UserCreate schema is just username.
    user_in = schemas.UserCreate(username=username)
    return crud.create_user(db=db, user_in=user_in)

# Helper function to create a prompt for tests
def create_test_prompt(db: Session, base_prompt_text: str = "Test base prompt", user_id: int = None) -> models.Prompt:
    prompt_in = schemas.PromptCreate(base_prompt=base_prompt_text, user_id=user_id)
    return crud.create_prompt(db=db, prompt_in=prompt_in)


# User CRUD Tests
def test_create_user(db_session: Session):
    user_in = schemas.UserCreate(username="newuser")
    user = crud.create_user(db=db_session, user_in=user_in)
    assert user is not None
    assert user.username == "newuser"
    assert user.id is not None

    fetched_user = db_session.get(models.User, user.id)
    assert fetched_user is not None
    assert fetched_user.username == "newuser"

def test_get_user(db_session: Session):
    user = create_test_user(db_session, username="getmeuser")
    fetched_user = crud.get_user(db=db_session, user_id=user.id)
    assert fetched_user is not None
    assert fetched_user.id == user.id
    assert fetched_user.username == "getmeuser"

def test_get_user_by_username(db_session: Session):
    create_test_user(db_session, username="findmeuser")
    fetched_user = crud.get_user_by_username(db=db_session, username="findmeuser")
    assert fetched_user is not None
    assert fetched_user.username == "findmeuser"

def test_update_user(db_session: Session):
    user = create_test_user(db_session, username="oldusername")
    user_update_in = schemas.UserUpdate(username="newusername")
    updated_user = crud.update_user(db=db_session, user_db=user, user_in=user_update_in)
    assert updated_user.username == "newusername"

    # Verify in DB
    refreshed_user = db_session.get(models.User, user.id)
    assert refreshed_user.username == "newusername"

def test_delete_user(db_session: Session):
    user = create_test_user(db_session, username="deletemeuser")
    deleted_user = crud.delete_user(db=db_session, user_id=user.id)
    assert deleted_user is not None
    assert deleted_user.id == user.id

    fetched_user = crud.get_user(db=db_session, user_id=user.id)
    assert fetched_user is None


# Prompt CRUD Tests
def test_create_prompt_without_user(db_session: Session):
    prompt_in = schemas.PromptCreate(base_prompt="A cool new prompt")
    prompt = crud.create_prompt(db=db_session, prompt_in=prompt_in)
    assert prompt is not None
    assert prompt.base_prompt == "A cool new prompt"
    assert prompt.user_id is None
    assert prompt.id is not None

def test_create_prompt_with_user(db_session: Session):
    user = create_test_user(db_session)
    prompt_in = schemas.PromptCreate(base_prompt="A prompt by a user", user_id=user.id)
    prompt = crud.create_prompt(db=db_session, prompt_in=prompt_in)
    assert prompt is not None
    assert prompt.base_prompt == "A prompt by a user"
    assert prompt.user_id == user.id

def test_get_prompt(db_session: Session):
    prompt = create_test_prompt(db_session, base_prompt_text="get this prompt")
    fetched_prompt = crud.get_prompt(db=db_session, prompt_id=prompt.id)
    assert fetched_prompt is not None
    assert fetched_prompt.id == prompt.id
    assert fetched_prompt.base_prompt == "get this prompt"

def test_get_prompts_by_user(db_session: Session):
    user1 = create_test_user(db_session, username="user1_prompts")
    user2 = create_test_user(db_session, username="user2_prompts")

    create_test_prompt(db_session, user_id=user1.id, base_prompt_text="p1_user1")
    create_test_prompt(db_session, user_id=user1.id, base_prompt_text="p2_user1")
    create_test_prompt(db_session, user_id=user2.id, base_prompt_text="p1_user2")

    user1_prompts = crud.get_prompts_by_user(db=db_session, user_id=user1.id)
    assert len(user1_prompts) == 2
    assert user1_prompts[0].base_prompt.startswith("p") # Basic check
    assert user1_prompts[0].user_id == user1.id

    user2_prompts = crud.get_prompts_by_user(db=db_session, user_id=user2.id)
    assert len(user2_prompts) == 1

    # Test pagination (simple check)
    limited_prompts = crud.get_prompts_by_user(db=db_session, user_id=user1.id, limit=1)
    assert len(limited_prompts) == 1

def test_get_all_prompts(db_session: Session):
    create_test_prompt(db_session, base_prompt_text="prompt A")
    create_test_prompt(db_session, base_prompt_text="prompt B")

    all_prompts = crud.get_all_prompts(db=db_session)
    assert len(all_prompts) == 2

    limited_prompts = crud.get_all_prompts(db=db_session, limit=1)
    assert len(limited_prompts) == 1

    # Add more for offset test
    create_test_prompt(db_session, base_prompt_text="prompt C")
    offset_prompts = crud.get_all_prompts(db=db_session, skip=1, limit=1)
    assert len(offset_prompts) == 1
    # Could check specific content if order is guaranteed or sorted

def test_update_prompt(db_session: Session):
    prompt = create_test_prompt(db_session, base_prompt_text="Original prompt text")
    prompt_update_in = schemas.PromptUpdate(base_prompt="Updated prompt text")
    updated_prompt = crud.update_prompt(db=db_session, prompt_db=prompt, prompt_in=prompt_update_in)
    assert updated_prompt.base_prompt == "Updated prompt text"

    refreshed_prompt = db_session.get(models.Prompt, prompt.id)
    assert refreshed_prompt.base_prompt == "Updated prompt text"

def test_delete_prompt(db_session: Session):
    prompt = create_test_prompt(db_session, base_prompt_text="deletable prompt")
    deleted_prompt = crud.delete_prompt(db=db_session, prompt_id=prompt.id)
    assert deleted_prompt is not None
    assert deleted_prompt.id == prompt.id

    fetched_prompt = crud.get_prompt(db=db_session, prompt_id=prompt.id)
    assert fetched_prompt is None


# QuestionnaireResponse CRUD Tests
def test_create_questionnaire_response(db_session: Session):
    prompt = create_test_prompt(db_session)
    qr_in = schemas.QuestionnaireResponseCreate(
        prompt_id=prompt.id, question="What is your quest?", answer="To seek the Holy Grail."
    )
    qr = crud.create_questionnaire_response(db=db_session, response_in=qr_in)
    assert qr is not None
    assert qr.prompt_id == prompt.id
    assert qr.question == "What is your quest?"
    assert qr.answer == "To seek the Holy Grail."

def test_create_multiple_questionnaire_responses(db_session: Session):
    prompt = create_test_prompt(db_session)
    responses_in_data = [
        {"question": "Q1", "answer": "A1"},
        {"question": "Q2", "answer": "A2"},
    ]
    # Convert to schemas.QuestionnaireResponseCreate, ensuring prompt_id is set
    responses_in_schemas = [
        schemas.QuestionnaireResponseCreate(prompt_id=prompt.id, **data) for data in responses_in_data
    ]

    # The crud function `create_multiple_questionnaire_responses` takes prompt_id_override.
    # So the prompt_id in responses_in_schemas will be overridden, which is fine.
    created_responses = crud.create_multiple_questionnaire_responses(
        db=db_session, responses_in=responses_in_schemas, prompt_id_override=prompt.id
    )
    assert len(created_responses) == 2
    for resp in created_responses:
        assert resp.prompt_id == prompt.id
        assert resp.id is not None

    db_prompt = crud.get_prompt(db=db_session, prompt_id=prompt.id)
    db_session.refresh(db_prompt) # Ensure relationships are loaded
    # This check might be more for API layer or if CRUD explicitly loads them.
    # Here, we check the DB directly.
    qrs_from_db = crud.get_questionnaire_responses_by_prompt(db=db_session, prompt_id=prompt.id)
    assert len(qrs_from_db) == 2


def test_get_questionnaire_responses_by_prompt(db_session: Session):
    prompt1 = create_test_prompt(db_session, base_prompt_text="prompt_qr1")
    prompt2 = create_test_prompt(db_session, base_prompt_text="prompt_qr2")

    qr_in1 = schemas.QuestionnaireResponseCreate(prompt_id=prompt1.id, question="Q_P1", answer="A_P1")
    crud.create_questionnaire_response(db=db_session, response_in=qr_in1)

    responses = crud.get_questionnaire_responses_by_prompt(db=db_session, prompt_id=prompt1.id)
    assert len(responses) == 1
    assert responses[0].question == "Q_P1"

    responses_prompt2 = crud.get_questionnaire_responses_by_prompt(db=db_session, prompt_id=prompt2.id)
    assert len(responses_prompt2) == 0


# ModelOutput CRUD Tests
def test_create_model_output(db_session: Session):
    prompt = create_test_prompt(db_session)
    mo_in = schemas.ModelOutputCreate(
        prompt_id=prompt.id, model_name="test_model", output="Test output from model."
    )
    mo = crud.create_model_output(db=db_session, output_in=mo_in)
    assert mo is not None
    assert mo.prompt_id == prompt.id
    assert mo.model_name == "test_model"
    assert mo.output == "Test output from model."

def test_get_model_outputs_by_prompt(db_session: Session):
    prompt1 = create_test_prompt(db_session, base_prompt_text="prompt_mo1")
    prompt2 = create_test_prompt(db_session, base_prompt_text="prompt_mo2")

    mo_in1 = schemas.ModelOutputCreate(prompt_id=prompt1.id, model_name="m1", output="o1_p1")
    crud.create_model_output(db=db_session, output_in=mo_in1)

    outputs = crud.get_model_outputs_by_prompt(db=db_session, prompt_id=prompt1.id)
    assert len(outputs) == 1
    assert outputs[0].model_name == "m1"

    outputs_prompt2 = crud.get_model_outputs_by_prompt(db=db_session, prompt_id=prompt2.id)
    assert len(outputs_prompt2) == 0
