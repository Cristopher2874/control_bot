import needle

@needle.tool
def get_weather(city: str):
    "Get the current weather for a city."
    return {"city": city, "temp_c": 27, "sky": "clear"}

@needle.tool
def write_essay(topic: str, length: str):
    """Write an essay using the existing LangChain LLM service."""
    from app.services.llm_service import get_llm_service

    prompt = f"Write an essay about the topic {topic} with a fixed length of {length}"

    response = get_llm_service().call_agent(prompt=prompt)

    return {"essay": response}
