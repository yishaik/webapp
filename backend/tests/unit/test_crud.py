import pytest
from sqlmodel import Session
from backend import crud, schemas, models

# Note: Fixtures like db_session are automatically available from conftest.py

def test_create_and_get_user(db_session: Session):
    user_in = schemas.UserCreate(username="testuser")
    db_user = crud.create_user(db=db_session, user=user_in)

    assert db_user.id is not None
    assert db_user.username == "testuser"

    retrieved_user = crud.get_user(db=db_session, user_id=db_user.id)
    assert retrieved_user
    assert retrieved_user.id == db_user.id
    assert retrieved_user.username == db_user.username

    retrieved_by_username = crud.get_user_by_username(db=db_session, username="testuser")
    assert retrieved_by_username
    assert retrieved_by_username.id == db_user.id

def test_get_user_not_found(db_session: Session):
    assert crud.get_user(db=db_session, user_id=999) is None
    assert crud.get_user_by_username(db=db_session, username="nouser") is None

def test_create_and_get_prompt_no_user(db_session: Session):
    prompt_in = schemas.PromptCreate(base_prompt="This is a test prompt.")
    # user_id is optional in PromptCreate for this call, will be set by crud function
    db_prompt = crud.create_prompt(db=db_session, prompt=prompt_in, user_id=None)

    assert db_prompt.id is not None
    assert db_prompt.base_prompt == "This is a test prompt."
    assert db_prompt.user_id is None
    assert db_prompt.timestamp is not None

    retrieved_prompt = crud.get_prompt(db=db_session, prompt_id=db_prompt.id)
    assert retrieved_prompt
    assert retrieved_prompt.id == db_prompt.id
    assert retrieved_prompt.base_prompt == db_prompt.base_prompt

def test_create_and_get_prompt_with_user(db_session: Session):
    user_in = schemas.UserCreate(username="promptuser")
    db_user = crud.create_user(db=db_session, user=user_in)

    prompt_in = schemas.PromptCreate(base_prompt="Prompt for user.")
    db_prompt = crud.create_prompt(db=db_session, prompt=prompt_in, user_id=db_user.id)

    assert db_prompt.user_id == db_user.id
    retrieved_prompt = crud.get_prompt(db=db_session, prompt_id=db_prompt.id)
    assert retrieved_prompt
    assert retrieved_prompt.user_id == db_user.id
    # Check relationships (lazy loading should work within session)
    assert retrieved_prompt.user
    assert retrieved_prompt.user.username == "promptuser"


def test_get_prompts(db_session: Session):
    crud.create_prompt(db=db_session, prompt=schemas.PromptCreate(base_prompt="p1"), user_id=None)
    crud.create_prompt(db=db_session, prompt=schemas.PromptCreate(base_prompt="p2"), user_id=None)

    all_prompts = crud.get_prompts(db=db_session, skip=0, limit=10)
    assert len(all_prompts) == 2

    limited_prompts = crud.get_prompts(db=db_session, skip=0, limit=1)
    assert len(limited_prompts) == 1
    assert limited_prompts[0].base_prompt == "p1" # Assuming order by ID / insertion

    skipped_prompts = crud.get_prompts(db=db_session, skip=1, limit=1)
    assert len(skipped_prompts) == 1
    assert skipped_prompts[0].base_prompt == "p2"


def test_get_prompts_by_user(db_session: Session):
    user1 = crud.create_user(db=db_session, user=schemas.UserCreate(username="user1"))
    user2 = crud.create_user(db=db_session, user=schemas.UserCreate(username="user2"))

    crud.create_prompt(db=db_session, prompt=schemas.PromptCreate(base_prompt="u1p1"), user_id=user1.id)
    crud.create_prompt(db=db_session, prompt=schemas.PromptCreate(base_prompt="u1p2"), user_id=user1.id)
    crud.create_prompt(db=db_session, prompt=schemas.PromptCreate(base_prompt="u2p1"), user_id=user2.id)

    user1_prompts = crud.get_prompts_by_user(db=db_session, user_id=user1.id)
    assert len(user1_prompts) == 2
    assert all(p.user_id == user1.id for p in user1_prompts)

    user2_prompts = crud.get_prompts_by_user(db=db_session, user_id=user2.id)
    assert len(user2_prompts) == 1


def test_create_and_get_questionnaire_response(db_session: Session):
    prompt = crud.create_prompt(db=db_session, prompt=schemas.PromptCreate(base_prompt="QR Test Prompt"))
    qr_in = schemas.QuestionnaireResponseCreate(question="Q1?", answer="A1.")

    db_qr = crud.create_questionnaire_response(db=db_session, response=qr_in, prompt_id=prompt.id)
    assert db_qr.id is not None
    assert db_qr.prompt_id == prompt.id
    assert db_qr.question == "Q1?"
    assert db_qr.answer == "A1."

    retrieved_qrs = crud.get_questionnaire_responses_by_prompt(db=db_session, prompt_id=prompt.id)
    assert len(retrieved_qrs) == 1
    assert retrieved_qrs[0].id == db_qr.id
    assert retrieved_qrs[0].answer == "A1."
    # Check relationship
    assert retrieved_qrs[0].prompt
    assert retrieved_qrs[0].prompt.id == prompt.id


def test_create_multiple_questionnaire_responses(db_session: Session):
    prompt = crud.create_prompt(db=db_session, prompt=schemas.PromptCreate(base_prompt="Multi QR Test"))
    qrs_in = [
        schemas.QuestionnaireResponseCreate(question="Q1", answer="A1"),
        schemas.QuestionnaireResponseCreate(question="Q2", answer="A2")
    ]
    db_qrs = crud.create_multiple_questionnaire_responses(db=db_session, responses=qrs_in, prompt_id=prompt.id)
    assert len(db_qrs) == 2
    assert all(qr.prompt_id == prompt.id for qr in db_qrs)

    retrieved_qrs = crud.get_questionnaire_responses_by_prompt(db=db_session, prompt_id=prompt.id)
    assert len(retrieved_qrs) == 2
    assert {qr.question for qr in retrieved_qrs} == {"Q1", "Q2"}

def test_create_and_get_model_output(db_session: Session):
    prompt = crud.create_prompt(db=db_session, prompt=schemas.PromptCreate(base_prompt="Model Output Test"))
    mo_in = schemas.ModelOutputCreate(model_name="TestModel", output="This is the output.")

    db_mo = crud.create_model_output(db=db_session, output=mo_in, prompt_id=prompt.id)
    assert db_mo.id is not None
    assert db_mo.prompt_id == prompt.id
    assert db_mo.model_name == "TestModel"
    assert db_mo.output == "This is the output."
    assert db_mo.timestamp is not None

    retrieved_mos = crud.get_model_outputs_by_prompt(db=db_session, prompt_id=prompt.id)
    assert len(retrieved_mos) == 1
    assert retrieved_mos[0].id == db_mo.id
    assert retrieved_mos[0].output == "This is the output."
    # Check relationship
    assert retrieved_mos[0].prompt
    assert retrieved_mos[0].prompt.id == prompt.id

def test_relationships_prompt_with_details(db_session: Session):
    # Create user, prompt, QRs, and MOs
    user = crud.create_user(db=db_session, user=schemas.UserCreate(username="detailuser"))
    prompt = crud.create_prompt(db=db_session, prompt=schemas.PromptCreate(base_prompt="Detailed Prompt"), user_id=user.id)
    crud.create_multiple_questionnaire_responses(db=db_session, responses=[
        schemas.QuestionnaireResponseCreate(question="Q1", answer="A1"),
        schemas.QuestionnaireResponseCreate(question="Q2", answer="A2"),
    ], prompt_id=prompt.id)
    crud.create_model_output(db=db_session, output=schemas.ModelOutputCreate(model_name="M1", output="O1"), prompt_id=prompt.id)
    crud.create_model_output(db=db_session, output=schemas.ModelOutputCreate(model_name="M2", output="O2"), prompt_id=prompt.id)

    # Retrieve the prompt
    retrieved_prompt = crud.get_prompt(db=db_session, prompt_id=prompt.id)
    assert retrieved_prompt is not None

    # SQLModel should lazy-load these when accessed within the session
    assert retrieved_prompt.user is not None
    assert retrieved_prompt.user.username == "detailuser"

    assert len(retrieved_prompt.questionnaire_responses) == 2
    assert {qr.question for qr in retrieved_prompt.questionnaire_responses} == {"Q1", "Q2"}

    assert len(retrieved_prompt.model_outputs) == 2
    assert {mo.model_name for mo in retrieved_prompt.model_outputs} == {"M1", "M2"}
