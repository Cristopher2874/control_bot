from langchain_core.messages import HumanMessage
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver

from config.llm_service_providers import LLM_SERVICE_PROVIDERS
from services.tools.tools import TOOLS

class LLMService:

    SYSTEM_PROMPT = "You are a helpful assistant. Be concise with responses"

    def __init__(self):
        self.active_model = LLM_SERVICE_PROVIDERS.get("light")
        self.tools = TOOLS
        self.checkpointer = InMemorySaver()
        self.agent_config = self._set_agent_config("1")
        self.agent = self._init_agent(model=self.active_model)

    def _init_agent(self,model:str=""):
        agent = create_agent(
            model=model,
            tools=self.tools,
            system_prompt=self.SYSTEM_PROMPT,
            checkpointer=self.checkpointer
        )

        return agent

    def _set_agent_config(self, chat_id: int | str | None = None):
        agent_config = {
            "configurable":{
                "thread_id": chat_id
            }
        }

        return agent_config

    def set_active_model(self, model:str="light"):
        self.active_model = model
        self.agent = self._init_agent(model=model)

    def get_active_model(self):
        return self.active_model

    def call_agent(self, prompt:str, chat_id: int | str | None = None):
        self._set_agent_config(chat_id=chat_id)
        try:
            response = self.agent.invoke(
                {"messages": [HumanMessage(prompt)]},
                config=self.agent_config
            )
        except Exception as e:
            return f"error executing agent: {e}"
        return response["messages"][-1].content_blocks