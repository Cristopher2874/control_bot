import needle
import logging

from app.utils.prompts import ESSAY_TOOL_PROMPT

logger = logging.getLogger(__name__)

@needle.tool
def get_weather(city: str):
    "Get the current weather for a city."
    return {"city": city, "temp_c": 27, "sky": "clear"}

@needle.tool
def write_essay(topic: str, length: str):
    """Write an essay based on a given topic and provided lenght for it, returns the final essay"""
    from app.services.llm_service import get_llm_service

    prompt = ESSAY_TOOL_PROMPT + f"\nTopic: {topic}" + f"\nLength: {length}"

    logger.info("Calling essay LLM")

    response = get_llm_service().call_agent(prompt=prompt)

    logger.info("Response generated from essay LLM")

    return {"essay": response}

TOOLS = [get_weather, write_essay]