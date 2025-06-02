from fastapi.testclient import TestClient
from sqlmodel import Session # For type hinting if needed, client fixture provides session via override
from typing import List, Dict, Any

from backend import schemas, crud, models # For creating test data directly or verifying types

# Helper to create a user directly via CRUD for test setup if needed
def setup_user(db: Session, username: str = "api_test_user") -> models.User:
    user_in = schemas.UserCreate(username=username)
    return crud.create_user(db=db, user_in=user_in)

# Helper to create a prompt directly via CRUD
def setup_prompt(db: Session, base_text: str = "API test prompt", user_id: int = None) -> models.Prompt:
    prompt_in = schemas.PromptCreate(base_prompt=base_text, user_id=user_id)
    return crud.create_prompt(db=db, prompt_in=prompt_in)

# Helper to create questionnaire responses directly via CRUD
def setup_questionnaire_responses(db: Session, prompt_id: int, count: int = 1) -> List[models.QuestionnaireResponse]:
    responses = []
    for i in range(count):
        qr_in = schemas.QuestionnaireResponseCreate(
            prompt_id=prompt_id, question=f"Q{i+1} for prompt {prompt_id}", answer=f"A{i+1}"
        )
        responses.append(crud.create_questionnaire_response(db=db, response_in=qr_in))
    return responses

# Helper to create model outputs directly via CRUD
def setup_model_outputs(db: Session, prompt_id: int, count: int = 1) -> List[models.ModelOutput]:
    outputs = []
    for i in range(count):
        mo_in = schemas.ModelOutputCreate(
            prompt_id=prompt_id, model_name=f"model_{i+1}", output=f"Output {i+1} for prompt {prompt_id}"
        )
        outputs.append(crud.create_model_output(db=db, output_in=mo_in))
    return outputs


# API Tests - History Endpoints
def test_api_list_all_prompts_empty(client: TestClient):
    response = client.get("/history/prompts")
    assert response.status_code == 200
    assert response.json() == []

def test_api_list_all_prompts_with_data(client: TestClient, db_session: Session): # db_session for setup
    setup_prompt(db_session, base_text="Prompt 1 for API history")
    setup_prompt(db_session, base_text="Prompt 2 for API history")

    response = client.get("/history/prompts")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["base_prompt"] == "Prompt 1 for API history"
    assert data[1]["base_prompt"] == "Prompt 2 for API history"

def test_api_get_full_prompt_details_not_found(client: TestClient):
    response = client.get("/history/prompt/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Prompt not found"}

def test_api_get_full_prompt_details_success(client: TestClient, db_session: Session):
    # Setup data
    prompt = setup_prompt(db_session, base_text="Detailed prompt")
    setup_questionnaire_responses(db_session, prompt_id=prompt.id, count=2)
    setup_model_outputs(db_session, prompt_id=prompt.id, count=1)

    response = client.get(f"/history/prompt/{prompt.id}")
    assert response.status_code == 200
    data = response.json()

    assert data["id"] == prompt.id
    assert data["base_prompt"] == "Detailed prompt"
    assert len(data["questionnaire_responses"]) == 2
    assert data["questionnaire_responses"][0]["question"] == f"Q1 for prompt {prompt.id}"
    assert len(data["model_outputs"]) == 1
    assert data["model_outputs"][0]["model_name"] == "model_1"


# API Tests - Interaction Endpoints
def test_api_submit_questionnaire_success(client: TestClient):
    request_payload = {
        "base_prompt": "New prompt from questionnaire",
        "user_id": None, # Or provide a user_id if a user is created/exists
        "responses": [
            {"question": "Q1", "answer": "A1 from API"},
            {"question": "Q2", "answer": "A2 from API"},
        ]
    }
    response = client.post("/questionnaires/submit", json=request_payload)
    assert response.status_code == 200 # As per current main.py (FastAPI default is 200 for POST)

    data = response.json()
    assert data["base_prompt"] == "New prompt from questionnaire"
    assert data["id"] is not None
    prompt_id = data["id"]

    assert len(data["questionnaire_responses"]) == 2
    assert data["questionnaire_responses"][0]["question"] == "Q1"
    assert data["questionnaire_responses"][0]["answer"] == "A1 from API"

    # Verify in DB (optional, but good for thoroughness, requires db_session)
    # For this, we'd need db_session fixture here too. Let's assume client tests focus on API contract.
    # If db_session is added:
    #   db_prompt = crud.get_prompt(db_session, prompt_id)
    #   assert db_prompt is not None
    #   qrs = crud.get_questionnaire_responses_by_prompt(db_session, prompt_id)
    #   assert len(qrs) == 2

def test_api_submit_questionnaire_invalid_data(client: TestClient):
    # Invalid payload: 'responses' is not a list
    request_payload = {
        "base_prompt": "This will fail",
        "responses": {"question": "Q1", "answer": "A1"}
    }
    response = client.post("/questionnaires/submit", json=request_payload)
    assert response.status_code == 422 # Unprocessable Entity for Pydantic validation errors

def test_api_record_model_output_prompt_not_found(client: TestClient):
    output_payload = {"model_name": "test_model", "output": "Some output"}
    response = client.post("/prompts/888/model_outputs", json=output_payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "Prompt not found, cannot record model output."

def test_api_record_model_output_success(client: TestClient, db_session: Session):
    prompt = setup_prompt(db_session, base_text="Prompt for model output")

    output_payload = {"model_name": "gpt-4", "output": "Generated text by gpt-4"}
    response = client.post(f"/prompts/{prompt.id}/model_outputs", json=output_payload)
    assert response.status_code == 200

    data = response.json()
    assert data["model_name"] == "gpt-4"
    assert data["output"] == "Generated text by gpt-4"
    assert data["prompt_id"] == prompt.id
    assert data["id"] is not None

    # Verify in DB (optional, as above)
    #   model_outputs = crud.get_model_outputs_by_prompt(db_session, prompt_id=prompt.id)
    #   assert len(model_outputs) == 1
    #   assert model_outputs[0].model_name == "gpt-4"

def test_api_record_model_output_invalid_data(client: TestClient, db_session: Session):
    prompt = setup_prompt(db_session, base_text="Prompt for invalid model output")

    # Invalid payload: 'model_name' is missing
    output_payload = {"output": "Missing model name"}
    response = client.post(f"/prompts/{prompt.id}/model_outputs", json=output_payload)
    assert response.status_code == 422


# Example of how to use db_session in an API test if direct DB verification is desired
# This test is redundant with test_api_submit_questionnaire_success but shows db_session usage
def test_api_submit_questionnaire_and_verify_in_db(client: TestClient, db_session: Session):
    request_payload = {
        "base_prompt": "Verify DB prompt",
        "user_id": None,
        "responses": [{"question": "Q_DB", "answer": "A_DB"}]
    }
    response = client.post("/questionnaires/submit", json=request_payload)
    assert response.status_code == 200

    data = response.json()
    prompt_id = data["id"]

    # Verification directly using CRUD and db_session
    retrieved_prompt = crud.get_prompt(db=db_session, prompt_id=prompt_id)
    assert retrieved_prompt is not None
    assert retrieved_prompt.base_prompt == "Verify DB prompt"

    retrieved_qrs = crud.get_questionnaire_responses_by_prompt(db=db_session, prompt_id=prompt_id)
    assert len(retrieved_qrs) == 1
    assert retrieved_qrs[0].question == "Q_DB"
