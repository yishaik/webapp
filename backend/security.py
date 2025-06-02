import secrets
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from backend.config import BASIC_AUTH_USERNAME, BASIC_AUTH_PASSWORD

security = HTTPBasic()

def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = BASIC_AUTH_USERNAME.encode("utf8")
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )

    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = BASIC_AUTH_PASSWORD.encode("utf8")
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )

    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password", # Changed detail message slightly for clarity
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# Optional: A simple User model for the authenticated user if needed later
class AuthenticatedUser:
    def __init__(self, username: str):
        self.username = username

def get_current_active_user(username: str = Depends(verify_credentials)):
    # In a more complex app, this function might load user details from the DB
    # For this task, simply returning an AuthenticatedUser object or just username is fine.
    return AuthenticatedUser(username)
