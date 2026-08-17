# llm_service.py
from __future__ import annotations

import threading
from typing import Dict

from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

import config

# Keep one active model per Telegram chat, so each conversation can switch models
# without accidentally affecting the rest of the message stream.
ACTIVE_MODELS: Dict[int, str] = {}
MODEL_CACHE: Dict[str, ChatOllama] = {}
MODEL_LOCK = threading.Lock()


def resolve_model_name(model_name: str | None) -> str:
    """Convert a friendly alias like 'gemma' or 'light' into a valid Ollama model name."""
    if model_name is None:
        return config.AVAILABLE_MODELS[config.DEFAULT_MODEL]

    normalized = model_name.strip().lower().replace(" ", "")
    if not normalized:
        return config.AVAILABLE_MODELS[config.DEFAULT_MODEL]

    if normalized in config.AVAILABLE_MODELS:
        return config.AVAILABLE_MODELS[normalized]

    if normalized in {value.lower(): value for value in config.AVAILABLE_MODELS.values()}:
        return {value.lower(): value for value in config.AVAILABLE_MODELS.values()}[normalized]

    available = ", ".join(sorted(config.AVAILABLE_MODELS.keys()))
    raise ValueError(
        f"Unknown model '{model_name}'. Available options: {available}. "
        "Use names like 'gemma', 'light', or a direct Ollama tag like 'gemma4:e2b'."
    )


def get_active_model(chat_id: int | str | None = None) -> str:
    """Return the model active for the provided chat ID. If none is set, use the default."""
    if chat_id is None:
        return config.AVAILABLE_MODELS[config.DEFAULT_MODEL]

    chat_key = int(chat_id)
    model_name = ACTIVE_MODELS.get(chat_key)
    if model_name is None:
        return config.AVAILABLE_MODELS[config.DEFAULT_MODEL]

    return resolve_model_name(model_name)


def set_active_model(chat_id: int | str, model_name: str) -> str:
    """Store the model to use for a specific Telegram chat."""
    resolved_model = resolve_model_name(model_name)
    ACTIVE_MODELS[int(chat_id)] = resolved_model
    return resolved_model


def get_llm_for_model(model_name: str) -> ChatOllama:
    """Create one cached ChatOllama instance per model to keep switching fast and stable."""
    resolved_model = resolve_model_name(model_name)

    with MODEL_LOCK:
        cached = MODEL_CACHE.get(resolved_model)
        if cached is None:
            cached = ChatOllama(
                model=resolved_model,
                base_url=config.OLLAMA_BASE_URL,
                temperature=0.7,
            )
            MODEL_CACHE[resolved_model] = cached

        return cached


def generate_response(prompt: str, chat_id: int | str | None = None) -> str:
    """
    Sends the prompt to the active local Ollama model for that chat and returns the response.
    Includes error handling to catch execution failures.
    """
    try:
        model_name = get_active_model(chat_id)
        llm = get_llm_for_model(model_name)
        messages = [HumanMessage(content=prompt)]
        response = llm.invoke(messages)
        return response.content
    except Exception as e:
        # This catches issues like Ollama being turned off or the model not existing.
        raise RuntimeError(f"LLM Execution Failed: {str(e)}")


if __name__ == "__main__":
    response = generate_response("Hello! What's the capital of France")
    print(response)