import pytest
from fastapi.testclient import TestClient
from sqlmodel import create_engine, Session, SQLModel
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
