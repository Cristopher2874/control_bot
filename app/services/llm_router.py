import needle

from app.services.tools.needle_tools import get_weather, write_essay

class LLMRouter:

    def __init__(self):
        self.agent = needle.Needle(tools=[get_weather, write_essay])

    def run_agent(self, prompt: str, chat_id: int | str | None = None) -> str:
        response = self.agent.run(query=prompt)
        return str(response)

_LLM_ROUTER = LLMRouter()

def get_llm_router() -> LLMRouter:
    return _LLM_ROUTER

def generate_response(prompt: str, chat_id: int | str) -> str:
    return _LLM_ROUTER.run_agent(prompt, chat_id=chat_id)