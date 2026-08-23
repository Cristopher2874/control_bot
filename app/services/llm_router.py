import needle
import logging

from app.services.tools.needle_tools import TOOLS

logger = logging.getLogger(__name__)

class LLMRouter:

    def __init__(self):
        self.tools = TOOLS
        self.agent = needle.Needle(tools=self.tools)
        logger.info("Started new LLM Router object")

    def run_agent(self, prompt: str, chat_id: int | str | None = None) -> str:
        logger.info(f"Calling router with prompt\n{prompt}")

        response = self.agent.run(query=prompt)
        
        logger.debug(response)
        logger.debug(str(type(response)))

        return str(response)

_LLM_ROUTER = LLMRouter()

def get_llm_router() -> LLMRouter:
    return _LLM_ROUTER

def generate_response(prompt: str, chat_id: int | str) -> str:
    return _LLM_ROUTER.run_agent(prompt, chat_id=chat_id)