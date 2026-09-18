import os
from dotenv import load_dotenv

# Load .env from the backend folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_FILE = os.path.join(BASE_DIR, ".env")

load_dotenv(ENV_FILE)


# ==========================================================
# GEMINI — 5 API KEYS
# ==========================================================

GEMINI_API_KEYS = [
    os.getenv("GEMINI_API_KEY_1", ""),
    os.getenv("GEMINI_API_KEY_2", ""),
    os.getenv("GEMINI_API_KEY_3", ""),
    os.getenv("GEMINI_API_KEY_4", ""),
    os.getenv("GEMINI_API_KEY_5", "")
]


GEMINI_MODELS = [
    os.getenv("GEMINI_MODEL_1", ""),
    os.getenv("GEMINI_MODEL_2", ""),
    os.getenv("GEMINI_MODEL_3", ""),
    os.getenv("GEMINI_MODEL_4", ""),
    os.getenv("GEMINI_MODEL_5", "")
]


# ==========================================================
# OPENROUTER — 5 API KEYS
# ==========================================================

OPENROUTER_API_KEYS = [
    os.getenv("OPENROUTER_API_KEY_1", ""),
    os.getenv("OPENROUTER_API_KEY_2", ""),
    os.getenv("OPENROUTER_API_KEY_3", ""),
    os.getenv("OPENROUTER_API_KEY_4", ""),
    os.getenv("OPENROUTER_API_KEY_5", "")
]


OPENROUTER_MODELS = [
    os.getenv("OPENROUTER_MODEL_1", "openrouter/free"),
    os.getenv("OPENROUTER_MODEL_2", "openrouter/free"),
    os.getenv("OPENROUTER_MODEL_3", "openrouter/free"),
    os.getenv("OPENROUTER_MODEL_4", "openrouter/free"),
    os.getenv("OPENROUTER_MODEL_5", "openrouter/free")
]


# ==========================================================
# PROVIDER SETTINGS
# ==========================================================

AI_PROVIDER = os.getenv("AI_PROVIDER", "multi")

GENERAL_PROVIDER = os.getenv("GENERAL_PROVIDER", "auto")
CODING_PROVIDER = os.getenv("CODING_PROVIDER", "auto")
MATH_PROVIDER = os.getenv("MATH_PROVIDER", "tool")
VOICE_PROVIDER = os.getenv("VOICE_PROVIDER", "auto")
VISION_PROVIDER = os.getenv("VISION_PROVIDER", "auto")


# ==========================================================
# RETRY / TIMEOUT
# ==========================================================

MAX_RETRIES = int(os.getenv("MAX_RETRIES", "2"))

MAX_CONVERSATION_MESSAGES = int(
    os.getenv("MAX_CONVERSATION_MESSAGES", "20")
)

REQUEST_TIMEOUT = int(
    os.getenv("REQUEST_TIMEOUT", "60")
)


# ==========================================================
# OPENROUTER
# ==========================================================

OPENROUTER_SITE_URL = os.getenv(
    "OPENROUTER_SITE_URL",
    ""
)

OPENROUTER_SITE_NAME = os.getenv(
    "OPENROUTER_SITE_NAME",
    "SK 2.0"
)


# ==========================================================
# ELEVENLABS
# ==========================================================

ELEVENLABS_API_KEY = os.getenv(
    "ELEVENLABS_API_KEY",
    ""
)

ELEVENLABS_VOICE_ID = os.getenv(
    "ELEVENLABS_VOICE_ID",
    ""
)


# ==========================================================
# OPENROUTER TTS
# ==========================================================

OPENROUTER_TTS_MODEL = os.getenv(
    "OPENROUTER_TTS_MODEL",
    ""
)

OPENROUTER_TTS_VOICE = os.getenv(
    "OPENROUTER_TTS_VOICE",
    ""
)


# ==========================================================
# APP INFORMATION
# ==========================================================

APP_NAME = os.getenv(
    "APP_NAME",
    "SK 2.0"
)

CREATED_BY = os.getenv(
    "CREATED_BY",
    "Abdul Rasheed Zahid"
)


# ==========================================================
# DEBUG
# ==========================================================

DEBUG_MODE = os.getenv(
    "DEBUG_MODE",
    "true"
).lower() == "true"


# ==========================================================
# SAFE CONFIG TEST
# ==========================================================

def show_config_status():
    print()
    print("================================")
    print("       SK 2.0 CONFIG")
    print("================================")

    for i, key in enumerate(GEMINI_API_KEYS, 1):
        status = "OK" if key else "EMPTY"
        print(f"Gemini API {i}: {status}")

    for i, key in enumerate(OPENROUTER_API_KEYS, 1):
        status = "OK" if key else "EMPTY"
        print(f"OpenRouter API {i}: {status}")

    print("================================")