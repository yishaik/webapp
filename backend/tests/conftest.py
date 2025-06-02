import pytest
from fastapi.testclient import TestClient
from sqlmodel import create_engine, Session, SQLModel, MetaData
from unittest.mock import patch
import os
from typing import Generator

# Attempt to provide a fresh MetaData object for the test session
SQLModel.metadata = MetaData() # Reset to a new MetaData for each test session/run

from backend.main import app, get_db
from backend import config

# 1. Mock API Keys
@pytest.fixture(scope="session", autouse=True)
def mock_api_keys_for_tests():
    mock_env_vars = {
        "OPENAI_API_KEY": "test_openai_key",
        "ANTHROPIC_API_KEY": "test_anthropic_key",
        "XAI_API_KEY": "test_xai_key",
        "GOOGLE_API_KEY": "test_google_key",
        "BASIC_AUTH_USERNAME": "testuser", # Ensure these are set for tests
        "BASIC_AUTH_PASSWORD": "testpass",   # Ensure these are set for tests
    }
    # Patch os.environ first
    with patch.dict(os.environ, mock_env_vars):
        # Then, patch the config module's attributes directly.
        # This is to handle cases where config might have already loaded values (e.g. defaults)
        # before os.environ was patched for the test session. `create=True` allows creating if not exist.
        with patch.object(config, 'OPENAI_API_KEY', 'test_openai_key', create=True), \
             patch.object(config, 'ANTHROPIC_API_KEY', 'test_anthropic_key', create=True), \
             patch.object(config, 'XAI_API_KEY', 'test_xai_key', create=True), \
             patch.object(config, 'GOOGLE_API_KEY', 'test_google_key', create=True), \
             patch.object(config, 'BASIC_AUTH_USERNAME', 'testuser', create=True), \
             patch.object(config, 'BASIC_AUTH_PASSWORD', 'testpass', create=True):
            # Reload settings in config if it uses a function to load them,
            # or ensure config module is re-imported/re-evaluated if necessary.
            # For this project, config.py loads on import, so patching os.environ before
            # most imports and patching config attributes should be robust.
            yield

# 2. Test Database Setup (Function-scoped engine and tables for full isolation)
@pytest.fixture(scope="function")
def test_engine_func_scope() -> Generator[create_engine, None, None]:
    # Each test function gets a completely new in-memory database
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    # The metadata should be the one from SQLModel (which we reset at the top)
    SQLModel.metadata.create_all(engine, checkfirst=True) # Added checkfirst=True
    yield engine
    SQLModel.metadata.drop_all(engine) # Ensure this also works as expected
    engine.dispose() # Dispose of the engine to close connections

@pytest.fixture(scope="function")
def db_session(test_engine_func_scope: create_engine) -> Generator[Session, None, None]:
    # Uses the function-scoped engine
    with Session(test_engine_func_scope) as session:
        yield session
    # No create_all/drop_all here, as it's handled by the engine fixture

# 3. Override get_db dependency and TestClient fixture
@pytest.fixture(scope="function")
def client(db_session: Session) -> Generator[TestClient, None, None]:
    def override_get_db() -> Generator[Session, None, None]:
        yield db_session

    original_get_db = app.dependency_overrides.get(get_db)
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    # Clean up dependency overrides
    if original_get_db:
        app.dependency_overrides[get_db] = original_get_db
    else:
        app.dependency_overrides.pop(get_db, None)
