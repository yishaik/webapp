import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import os

# Set environment variables for testing BEFORE importing main
os.environ['BASIC_AUTH_USERNAME'] = 'testuser'
os.environ['BASIC_AUTH_PASSWORD'] = 'testpass'

from backend.main import app # app must be imported after env vars are set

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="module")
def basic_auth_headers():
    return ('testuser', 'testpass')

# --- Test /generate_questionnaire ---
@patch('backend.main.generate_questions')
def test_generate_questionnaire_success(mock_generate_questions, client, basic_auth_headers):
    mock_generate_questions.return_value = ["Q1?", "Q2?"]
    response = client.post(
        "/generate_questionnaire",
        json={"base_prompt": "Test prompt"},
        auth=basic_auth_headers
    )
    assert response.status_code == 200
    assert response.json() == {"questions": ["Q1?", "Q2?"]}
    mock_generate_questions.assert_called_once_with("Test prompt")

def test_generate_questionnaire_auth_failure(client):
    response = client.post("/generate_questionnaire", json={"base_prompt": "Test prompt"})
    assert response.status_code == 401 # Unauthorized without auth

    response = client.post(
        "/generate_questionnaire",
        json={"base_prompt": "Test prompt"},
        auth=('wronguser', 'wrongpass')
    )
    assert response.status_code == 401 # Unauthorized with wrong auth

def test_generate_questionnaire_invalid_input(client, basic_auth_headers):
    response = client.post("/generate_questionnaire", json={}, auth=basic_auth_headers)
    assert response.status_code == 422 # Unprocessable Entity

    response = client.post("/generate_questionnaire", json={"base_prompt": 123}, auth=basic_auth_headers) # Not a string
    assert response.status_code == 422


# --- Test /submit_questionnaire ---
def test_submit_questionnaire_success(client, basic_auth_headers):
    # Clear in-memory db for this test if needed, or check length
    # For simplicity, we'll just check for a successful response structure
    initial_len = len(app.state.questionnaire_submissions_db if hasattr(app.state, 'questionnaire_submissions_db') else [])

    response = client.post(
        "/submit_questionnaire",
        json={"prompt": "Test prompt", "answers": ["Ans1", "Ans2"]},
        auth=basic_auth_headers
    )
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["message"] == "Questionnaire submitted successfully."
    assert "submission_id" in json_response

    # Check if submission was added to our in-memory list
    # Re-accessing the list from app directly. If main.py changes var name, this breaks.
    from backend.main import questionnaire_submissions_db as main_db
    assert len(main_db) == initial_len + 1
    assert main_db[-1]["prompt"] == "Test prompt"


def test_submit_questionnaire_auth_failure(client):
    response = client.post("/submit_questionnaire", json={"prompt": "Test", "answers": ["Ans"]})
    assert response.status_code == 401

def test_submit_questionnaire_invalid_input(client, basic_auth_headers):
    response = client.post("/submit_questionnaire", json={"prompt": "Test"}, auth=basic_auth_headers) # Missing answers
    assert response.status_code == 422

    response = client.post("/submit_questionnaire", json={"prompt": 123, "answers": "NotAList"}, auth=basic_auth_headers)
    assert response.status_code == 422


# --- Test /optimize_prompt ---
@patch('backend.main.optimize_prompt')
def test_optimize_prompt_success(mock_optimize_prompt, client, basic_auth_headers):
    mock_optimize_prompt.return_value = "Optimized: Test prompt"
    response = client.post(
        "/optimize_prompt",
        json={"initial_prompt": "Test prompt", "questionnaire_answers": ["Ans1"], "target_model": "gpt-3.5"},
        auth=basic_auth_headers
    )
    assert response.status_code == 200
    assert response.json() == {"optimized_prompt": "Optimized: Test prompt"}
    mock_optimize_prompt.assert_called_once_with(
        initial_prompt="Test prompt",
        questionnaire_answers=["Ans1"],
        target_model="gpt-3.5"
    )

def test_optimize_prompt_auth_failure(client):
    response = client.post("/optimize_prompt", json={"initial_prompt": "Test", "questionnaire_answers": [], "target_model": "m"})
    assert response.status_code == 401

def test_optimize_prompt_invalid_input(client, basic_auth_headers):
    response = client.post("/optimize_prompt", json={"initial_prompt": "Test"}, auth=basic_auth_headers) # Missing fields
    assert response.status_code == 422


# --- Test /recommend_models ---
@patch('backend.main.recommend_models')
def test_recommend_models_success(mock_recommend_models, client, basic_auth_headers):
    mock_recommend_models.return_value = ["model1", "model2"]
    response = client.post(
        "/recommend_models",
        json={"initial_prompt": "Test prompt", "questionnaire_answers": ["Ans1"]},
        auth=basic_auth_headers
    )
    assert response.status_code == 200
    assert response.json() == {"recommended_models": ["model1", "model2"]}
    mock_recommend_models.assert_called_once_with(
        initial_prompt="Test prompt",
        questionnaire_answers=["Ans1"]
    )

def test_recommend_models_auth_failure(client):
    response = client.post("/recommend_models", json={"initial_prompt": "Test", "questionnaire_answers": []})
    assert response.status_code == 401

def test_recommend_models_invalid_input(client, basic_auth_headers):
    response = client.post("/recommend_models", json={"initial_prompt": "Test"}, auth=basic_auth_headers) # Missing answers
    assert response.status_code == 422

# --- Test health and root endpoints (simple checks) ---
def test_root_authenticated(client, basic_auth_headers):
    response = client.get("/", auth=basic_auth_headers)
    assert response.status_code == 200
    assert response.json() == {"message": "Prompt Builder API is running"}

def test_root_unauthenticated(client):
    response = client.get("/")
    assert response.status_code == 401

def test_health_authenticated(client, basic_auth_headers):
    response = client.get("/health", auth=basic_auth_headers)
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_health_unauthenticated(client):
    response = client.get("/health")
    assert response.status_code == 401

# Fixture to reset the in-memory questionnaire_submissions_db before each test that uses it
# This is a bit tricky because the list is in main.py
@pytest.fixture(autouse=True)
def reset_submission_db():
    from backend.main import questionnaire_submissions_db
    original_content = list(questionnaire_submissions_db)
    questionnaire_submissions_db.clear()
    yield
    questionnaire_submissions_db.extend(original_content)


# It's important that the `app` from `backend.main` is the one used by TestClient.
# If `create_tables()` or other startup logic is problematic for tests or needs mocking,
# it might require further adjustments, e.g., by preventing auto-run on import for test environment.
# For now, assuming `create_tables()` is safe to run or doesn't interfere with these tests.
# The `BASIC_AUTH_USERNAME` and `PASSWORD` must be set before `backend.main` is imported.
# If `load_dotenv()` in `main.py` overwrites these, tests could fail.
# A common pattern is to have a separate `config.py` for settings and manage test settings there.

# Note on the in-memory questionnaire_submissions_db:
# The test_submit_questionnaire_success interacts with the actual list in main.py.
# The `reset_submission_db` fixture attempts to manage its state.
# If this becomes problematic, the list should be managed via app.state or a dependency
# that can be overridden during testing.
# For now, `app.state.questionnaire_submissions_db = []` is not how it's defined in main.py.
# It's a global list `questionnaire_submissions_db`.
# The fixture `reset_submission_db` directly manipulates this global list.
# This direct manipulation of a global list from another module is generally not ideal
# but done here for simplicity given the current structure of main.py.
# A better way would be to have `questionnaire_submissions_db` as part of `app.state`
# or managed through a dependency that can be overridden in tests.
# For example, in main.py: `app.state.questionnaire_submissions_db = []`
# Then in tests, you could access/clear `client.app.state.questionnaire_submissions_db`.
# I've updated the test_submit_questionnaire_success to reflect this if app.state was used.
# Since it is a global list, I've added a direct import and manipulation in the fixture.

# One final check on the /submit_questionnaire test:
# The `submission_id` returned is `len(questionnaire_submissions_db)`.
# If tests run in parallel (not default for pytest unless specified) or if the list is not properly cleared,
# this could lead to flaky tests. The autouse fixture `reset_submission_db` should help.
