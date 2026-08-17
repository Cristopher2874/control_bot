import os
from dotenv import load_dotenv

load_dotenv()

# config.py

# ==========================================
# PASTE YOUR TOKEN FROM BOTFATHER HERE
# ==========================================
BOT_TOKEN = os.getenv("BOT_SK_TOKEN")

OLLAMA_BASE_URL = "http://localhost:11434"

# Available local models for the bot.
# These names are user-friendly aliases and map to the real Ollama model names.
AVAILABLE_MODELS = {
    "light": "gemma4:e2b",
    "gemma-light": "gemma4:e2b",
    "gemma4:e2b": "gemma4:e2b",
    "heavy": "gemma4:e4b",
    "gemma": "gemma4:e4b",
    "gemma4:e4b": "gemma4:e4b",
    "gemma-cloud": "gemma4:31b-cloud",
}

DEFAULT_MODEL = "light"
OLLAMA_LIGHT_MODEL = AVAILABLE_MODELS["light"]
OLLAMA_MODEL = AVAILABLE_MODELS[DEFAULT_MODEL]