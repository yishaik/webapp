import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

# Fixtures 'client' and 'db_session' are from conftest.py
# Basic auth credentials from backend/security.py (hardcoded)
TEST_AUTH = ("admin", "password123")
INVALID_AUTH = ("wrong", "user")

# --- Health and Basic Auth Tests ---
def test_health_check(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_root_endpoint(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Prompt Builder API is running"}

def test_protected_endpoint_no_auth(client: TestClient):
    # Example: /history/prompts requires auth
    response = client.get("/history/prompts")
    assert response.status_code == 401 # Expecting Unauthorized

def test_protected_endpoint_invalid_auth(client: TestClient):
    response = client.get("/history/prompts", auth=INVALID_AUTH)
    assert response.status_code == 401

# --- Questionnaire Endpoints ---
def test_generate_questionnaire(client: TestClient):
    payload = {"base_prompt": "Explain quantum physics."}
    response = client.post("/generate_questionnaire", json=payload, auth=TEST_AUTH)
    assert response.status_code == 200
    data = response.json()
    assert "questions" in data
    assert isinstance(data["questions"], list)
    assert len(data["questions"]) > 0 # Based on current questionnaire logic

def test_generate_questionnaire_empty_prompt(client: TestClient):
    payload = {"base_prompt": ""}
    response = client.post("/generate_questionnaire", json=payload, auth=TEST_AUTH)
    assert response.status_code == 200 # Endpoint might accept, logic in generate_questions handles it
    data = response.json()
    assert "questions" in data
    # Logic in generate_questions should still produce questions like "prompt is short"

def test_submit_questionnaire(client: TestClient, db_session): # db_session for potential verification
    payload = {
        "base_prompt": "My new project idea.",
        "responses": [
            {"question": "What is the target audience?", "answer": "Developers"},
            {"question": "Desired output format?", "answer": "JSON"}
        ]
    }
    response = client.post("/submit_questionnaire", json=payload, auth=TEST_AUTH)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["base_prompt"] == "My new project idea."
    assert len(data["questionnaire_responses"]) == 2
    assert data["questionnaire_responses"][0]["question"] == "What is the target audience?"

    # Verify in DB (optional here, as CRUD is unit-tested)
    from backend import crud # For direct DB check if needed
    prompt_id = data["id"]
    db_prompt = crud.get_prompt(db=db_session, prompt_id=prompt_id)
    assert db_prompt is not None
    assert len(db_prompt.questionnaire_responses) == 2


# --- History Endpoints ---
def test_get_history_prompts_empty(client: TestClient):
    response = client.get("/history/prompts", auth=TEST_AUTH)
    assert response.status_code == 200
    assert response.json() == [] # Assuming clean DB from test_app_db_session

def test_get_history_prompts_with_data(client: TestClient):
    # First, create a prompt
    client.post("/submit_questionnaire", json={
        "base_prompt": "History test prompt", "responses": []
    }, auth=TEST_AUTH)

    response = client.get("/history/prompts", auth=TEST_AUTH)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["base_prompt"] == "History test prompt"

def test_get_history_prompt_details(client: TestClient):
    # Create a prompt with details
    submit_payload = {
        "base_prompt": "Detailed history prompt",
        "responses": [{"question": "Q1", "answer": "A1"}]
    }
    submit_response = client.post("/submit_questionnaire", json=submit_payload, auth=TEST_AUTH)
    prompt_id = submit_response.json()["id"]

    # Mock model output creation for this test as it's not part of this endpoint's direct test
    with patch("backend.crud.create_model_output") as mock_create_model_output:
        mock_create_model_output.return_value = None # Or a mock ModelOutput object
        # Example: Create a dummy model output via crud if needed, or rely on /get_model_response test
        # For now, this endpoint only shows prompt and QRs. Model outputs are via /get_model_response.

        detail_response = client.get(f"/history/prompt/{prompt_id}", auth=TEST_AUTH)
        assert detail_response.status_code == 200
        data = detail_response.json()
        assert data["id"] == prompt_id
        assert data["base_prompt"] == "Detailed history prompt"
        assert len(data["questionnaire_responses"]) == 1
        assert data["questionnaire_responses"][0]["question"] == "Q1"
        # model_outputs would be tested more thoroughly with /get_model_response tests

def test_get_history_prompt_details_not_found(client: TestClient):
    response = client.get("/history/prompt/9999", auth=TEST_AUTH)
    assert response.status_code == 404


# --- Optimization and Recommendation Endpoints ---
def test_recommend_models(client: TestClient):
    submit_response = client.post("/submit_questionnaire", json={
        "base_prompt": "Recommend models for coding a script.", "responses": []
    }, auth=TEST_AUTH)
    prompt_id = submit_response.json()["id"]

    recommend_payload = {"prompt_id": prompt_id}
    response = client.post("/recommend_models", json=recommend_payload, auth=TEST_AUTH)
    assert response.status_code == 200
    data = response.json()
    assert "models" in data
    assert isinstance(data["models"], list)
    assert len(data["models"]) > 0 # Expect some recommendations

def test_optimize_prompt(client: TestClient):
    submit_response = client.post("/submit_questionnaire", json={
        "base_prompt": "Optimize this simple prompt.", "responses": []
    }, auth=TEST_AUTH)
    prompt_id = submit_response.json()["id"]

    optimize_payload = {"prompt_id": prompt_id, "target_model": "any_model_for_test"}
    response = client.post("/optimize_prompt", json=optimize_payload, auth=TEST_AUTH)
    assert response.status_code == 200
    data = response.json()
    assert "optimized_prompt" in data
    assert "Optimize this simple prompt." in data["optimized_prompt"] # Base should be there
    assert "Act as an expert" in data["optimized_prompt"] # Optimizer adds this

# --- /get_model_response Endpoint (with mocking) ---
# This is where we mock the actual LLM handler calls
@patch("backend.api_handlers.openai_handler.get_llm_response")
@patch("backend.api_handlers.claude_handler.get_llm_response")
@patch("backend.api_handlers.grok_handler.get_llm_response")
@patch("backend.api_handlers.gemini_handler.get_llm_response")
def test_get_model_response_openai(
    mock_gemini, mock_grok, mock_claude, mock_openai, client: TestClient, db_session
):
    mock_openai.return_value = "Mocked OpenAI Output"

    # 1. Create a prompt first
    prompt_payload = {"base_prompt": "Test OpenAI", "responses": []}
    submit_res = client.post("/submit_questionnaire", json=prompt_payload, auth=TEST_AUTH)
    prompt_id = submit_res.json()["id"]

    # 2. Request model response
    model_req_payload = {"prompt_id": prompt_id, "model_name": "GPT-4.1"} # Friendly name
    response = client.post("/get_model_response", json=model_req_payload, auth=TEST_AUTH)

    assert response.status_code == 200
    data = response.json()
    assert data["prompt_id"] == prompt_id
    assert data["model_name"] == "GPT-4.1"
    assert data["output"] == "Mocked OpenAI Output"
    assert "Test OpenAI" in data["optimized_prompt_used"] # Check optimization was run

    mock_openai.assert_called_once()
    # The call check needs to match the actual SDK model name and optimized prompt
    # args, kwargs = mock_openai.call_args
    # assert kwargs['model_name'] == 'gpt-4o' # SDK name for GPT-4.1
    # assert "Test OpenAI" in kwargs['prompt'] # Optimized prompt

    # Verify ModelOutput was created
    from backend import crud
    outputs = crud.get_model_outputs_by_prompt(db=db_session, prompt_id=prompt_id)
    assert len(outputs) == 1
    assert outputs[0].model_name == "GPT-4.1"
    assert outputs[0].output == "Mocked OpenAI Output"


@patch("backend.api_handlers.claude_handler.get_llm_response")
def test_get_model_response_claude_handler_error(mock_claude, client: TestClient):
    mock_claude.return_value = "Error: Claude simulated error" # Handler's error format

    prompt_payload = {"base_prompt": "Test Claude Error", "responses": []}
    submit_res = client.post("/submit_questionnaire", json=prompt_payload, auth=TEST_AUTH)
    prompt_id = submit_res.json()["id"]

    model_req_payload = {"prompt_id": prompt_id, "model_name": "Claude Opus 4"}
    response = client.post("/get_model_response", json=model_req_payload, auth=TEST_AUTH)

    assert response.status_code == 502 # LLM API call failed
    data = response.json()
    assert "LLM API call failed: Error: Claude simulated error" in data["detail"]


def test_get_model_response_unsupported_model(client: TestClient):
    prompt_payload = {"base_prompt": "Test Unsupported", "responses": []}
    submit_res = client.post("/submit_questionnaire", json=prompt_payload, auth=TEST_AUTH)
    prompt_id = submit_res.json()["id"]

    model_req_payload = {"prompt_id": prompt_id, "model_name": "NonExistentModel-123"}
    response = client.post("/get_model_response", json=model_req_payload, auth=TEST_AUTH)
    assert response.status_code == 400
    assert "Model 'NonExistentModel-123' is not supported" in response.json()["detail"]

def test_get_model_response_prompt_not_found(client: TestClient):
    model_req_payload = {"prompt_id": 9999, "model_name": "GPT-4.1"}
    response = client.post("/get_model_response", json=model_req_payload, auth=TEST_AUTH)
    assert response.status_code == 404
    assert "Prompt with ID 9999 not found" in response.json()["detail"]
