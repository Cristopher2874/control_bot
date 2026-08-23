import needle
from app.services.llm_service import get_llm_service

@needle.tool
def get_weather(city: str):
    "Get the current weather for a city."
    return {"city": city, "temp_c": 27, "sky": "clear"}

@needle.tool
def write_essay(topic: str, lenght: str):
    "Given a topic and lenght parameters, writes an essay on string format."
    "The length is a string to inform the parameters"

    LLM_SERVICE = get_llm_service()

    prompt = f"Write an essay about the topic {topic} with a fixed lenght of {lenght}"

    response = LLM_SERVICE.call_agent(prompt=prompt)

    return {"essay": response}
