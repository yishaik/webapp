import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables from backend/.env
# This ensures that if this file is imported, it tries to load .env relative to its location.
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=dotenv_path)

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
XAI_API_KEY = os.getenv("XAI_API_KEY") # For Grok
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") # For Gemini

# Basic Authentication Credentials
BASIC_AUTH_USERNAME = os.getenv("BASIC_AUTH_USERNAME", "testuser")
BASIC_AUTH_PASSWORD = os.getenv("BASIC_AUTH_PASSWORD", "testpass")

# Log warnings for missing API keys
if not OPENAI_API_KEY:
    logging.warning("OPENAI_API_KEY not found in environment variables or backend/.env.")
if not ANTHROPIC_API_KEY:
    logging.warning("ANTHROPIC_API_KEY not found in environment variables or backend/.env.")
if not XAI_API_KEY:
    logging.warning("XAI_API_KEY not found in environment variables or backend/.env.")
if not GOOGLE_API_KEY:
    logging.warning("GOOGLE_API_KEY not found in environment variables or backend/.env.")

if BASIC_AUTH_USERNAME == "testuser" or BASIC_AUTH_PASSWORD == "testpass":
    logging.warning("Using default basic authentication credentials. It is recommended to set custom credentials in backend/.env.")
