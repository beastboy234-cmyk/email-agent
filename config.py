import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = "gpt-4o-mini"

# Gmail Configuration
GOOGLE_CLIENT_SECRET_PATH = os.getenv("GOOGLE_CLIENT_SECRET_PATH", "credentials/credentials.json")
TOKEN_PATH = os.getenv("TOKEN_PATH", "credentials/token.json")

# Gmail API Scopes
GMAIL_SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.compose",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.modify",
]

# Email Send Mode
EMAIL_SEND_MODE = os.getenv("EMAIL_SEND_MODE", "confirm_before_send")
assert EMAIL_SEND_MODE in [
    "draft_only",
    "confirm_before_send",
    "auto_send_allowed",
], "Invalid EMAIL_SEND_MODE"

# User Information
DEFAULT_USER_NAME = os.getenv("DEFAULT_USER_NAME", "User")
DEFAULT_SIGNATURE = os.getenv("DEFAULT_SIGNATURE", "")

# Logging
LOG_DIR = "logs"
ACTION_LOG_FILE = os.path.join(LOG_DIR, "actions.log")

# Create logs directory if it doesn't exist
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
