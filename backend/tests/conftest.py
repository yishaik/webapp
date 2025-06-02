import pytest
from fastapi.testclient import TestClient
from sqlmodel import create_engine, Session, SQLModel
<<<<<<< HEAD
from unittest.mock import patch
import os

# Import the main FastAPI app and the dependency override mechanism
# Adjust the import path based on your project structure.
# Assuming 'main.py' is in the 'backend' directory, and 'tests' is also in 'backend'.
from backend.main import app, get_session  # Main app and original get_session
from backend import config # To mock API keys

# 1. Mock API Keys before they are loaded by config.py
# This needs to happen as early as possible.
# We can patch os.getenv for the specific keys used in config.py
@pytest.fixture(scope="session", autouse=True)
def mock_api_keys_for_tests():
    # These environment variables would normally be loaded by dotenv in config.py
    # For tests, we explicitly set them to mock values or None if the service
    # should gracefully handle missing keys (which our handlers are designed to do).
    with patch.dict(os.environ, {
        "OPENAI_API_KEY": "test_openai_key",
        "ANTHROPIC_API_KEY": "test_anthropic_key",
        "XAI_API_KEY": "test_xai_key",
        "GOOGLE_API_KEY": "test_google_key",
    }):
        # Additionally, if config.py has already been imported and variables set,
        # we might need to patch the variables directly in the config module.
        # This ensures that even if config was imported before this fixture ran its course
        # (e.g. by another imported module at load time), the values are overridden.
        with patch.object(config, 'OPENAI_API_KEY', 'test_openai_key'), \
             patch.object(config, 'ANTHROPIC_API_KEY', 'test_anthropic_key'), \
             patch.object(config, 'XAI_API_KEY', 'test_xai_key'), \
             patch.object(config, 'GOOGLE_API_KEY', 'test_google_key'):
            yield

# 2. In-memory SQLite database fixture
# Using a session-scoped engine to create it once per test session.
# Individual test functions will get a new session from this engine.
SQLITE_DATABASE_URL_TEST = "sqlite:///:memory:"
test_engine = create_engine(
    SQLITE_DATABASE_URL_TEST,
    connect_args={"check_same_thread": False}, # Needed for SQLite
    echo=False # Can be True for debugging SQL
)

@pytest.fixture(scope="session")
def db_engine():
    # SQLModel.metadata.drop_all(test_engine) # Optional: ensure clean state if run multiple times locally
    SQLModel.metadata.create_all(test_engine)
    return test_engine

@pytest.fixture(scope="function") # Each test function gets a fresh session and transaction
def db_session(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection, autocommit=False, autoflush=False)
    yield session
    session.close()
    transaction.rollback() # Rollback changes after each test
    connection.close()


# 3. Override get_session dependency for API tests
# This fixture will provide a test session to the FastAPI app's dependencies.
@pytest.fixture(scope="function")
def test_app_db_session(db_session): # Depends on the db_session fixture
    # This is the session that will be injected into endpoint dependencies
    def override_get_session():
        try:
            yield db_session
        finally:
            # db_session fixture already handles close/rollback
            pass

    # Override the dependency in the app
    original_get_session = app.dependency_overrides.get(get_session)
    app.dependency_overrides[get_session] = override_get_session
    yield db_session # Provide the session to the test if needed directly

    # Restore original dependency (or clear it) after the test
    if original_get_session:
        app.dependency_overrides[get_session] = original_get_session
    else:
        del app.dependency_overrides[get_session]


# 4. TestClient fixture
# This uses the overridden get_session through test_app_db_session
@pytest.fixture(scope="function")
def client(test_app_db_session): # Ensures db session override is active
    # The TestClient will use the app with the overridden dependency
    with TestClient(app) as c:
        yield c

# Note: The order of fixtures and their scopes is important.
# mock_api_keys_for_tests (session, autouse=True) runs first.
# db_engine (session) sets up the database once.
# db_session (function) gives a transactional session to each test.
# test_app_db_session (function) overrides FastAPI's session for a test.
# client (function) uses the app with the overridden session.
=======
from typing import Generator

# Import your FastAPI app and the real get_session dependency
from backend.main import app
from backend.database import get_session # This is what we need to override

# Define the test database URL (in-memory SQLite)
TEST_DATABASE_URL = "sqlite:///:memory:"

# Create a test engine
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False}, echo=False) # echo=False for cleaner test output

# Fixture for a database session
@pytest.fixture(scope="function") # "function" scope for test isolation: db is clean for each test
def db_session() -> Generator[Session, None, None]:
    # Create tables for each test function
    SQLModel.metadata.create_all(test_engine)

    with Session(test_engine) as session:
        yield session

    # Drop tables after each test function to ensure isolation
    SQLModel.metadata.drop_all(test_engine)

# Fixture for the TestClient, using the db_session override
@pytest.fixture(scope="function") # Client should also be function-scoped if db is function-scoped
def client(db_session: Session) -> Generator[TestClient, None, None]:

    # Dependency override for get_session
    def get_session_override() -> Generator[Session, None, None]:
        yield db_session

    app.dependency_overrides[get_session] = get_session_override

    with TestClient(app) as test_client:
        yield test_client

    # Clean up dependency overrides
    app.dependency_overrides.clear()
>>>>>>> origin/master
