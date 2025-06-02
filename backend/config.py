import os
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
# Assuming .env file is in the same directory as this config.py, or in the root of the 'backend' package.
# If running from within 'backend' directory, './.env' or just '.env' is fine.
# If main.py is in 'backend' and config.py is also in 'backend', this should work.
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if not os.path.exists(dotenv_path):
    # Try one level up if .env is in the project root (e.g. /app/.env)
    # and this script is in /app/backend/config.py
    dotenv_path_parent = os.path.join(os.path.dirname(__file__), '..', '.env')
    if os.path.exists(dotenv_path_parent):
        dotenv_path = dotenv_path_parent
    else:
        # Fallback for environments where .env might not be present (e.g. CI/CD, production with direct env vars)
        logging.warning(f"'.env' file not found at {dotenv_path} or {dotenv_path_parent}. Relying on system environment variables.")

load_dotenv(dotenv_path=dotenv_path if os.path.exists(dotenv_path) else None, override=True)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
XAI_API_KEY = os.getenv("XAI_API_KEY") # For Grok
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") # For Gemini

# Basic logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# You can add a check here to ensure critical keys are loaded
if not OPENAI_API_KEY:
    logging.warning("OPENAI_API_KEY not found in environment variables.")
if not ANTHROPIC_API_KEY:
    logging.warning("ANTHROPIC_API_KEY not found in environment variables.")
if not XAI_API_KEY:
    logging.warning("XAI_API_KEY not found in environment variables.")
if not GOOGLE_API_KEY:
    logging.warning("GOOGLE_API_KEY not found in environment variables.")
