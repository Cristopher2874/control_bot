import os
from dotenv import load_dotenv
load_dotenv()

# config.py

# ==========================================
# PASTE YOUR TOKEN FROM BOTFATHER HERE
# ==========================================
BOT_TOKEN = os.getenv("BOT_SK_TOKEN")

# 1m - 8m
# OLLAMA_MODEL = "qwen3.5:2b"
# 1m - 3m easy questions
OLLAMA_LIGHT_MODEL = "gemma4:e2b"
# 5m - 7m complete responses and more accurate
OLLAMA_MODEL = "gemma4:e4b"
OLLAMA_BASE_URL = "http://localhost:11434"