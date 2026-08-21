from typing import Any

from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver

from app.config.llm_service_providers import LLM_SERVICE_PROVIDERS
from app.services.tools.tools import TOOLS


class LLMService:
    SYSTEM_PROMPT = "You are a helpful assistant. Be concise with responses"

    def __init__(self, default_model_alias: str = "light"):
        self.tools = TOOLS
        self.checkpointer = InMemorySaver()
        self.default_model = self.resolve_model_name(default_model_alias)
        self.active_model = self.default_model
        self.agent = self._init_agent(model=self.active_model)

    def _thread_id(self, chat_id: int | str | None = None) -> str:
        if chat_id is None:
            return "single-user"
        return str(chat_id)

    def _init_agent(self, model: str) -> Any:
        provider_model = model if model.startswith("ollama:") else f"ollama:{model}"
        return create_agent(
            model=provider_model,
            tools=self.tools,
            system_prompt=self.SYSTEM_PROMPT,
            checkpointer=self.checkpointer,
        )

    def _build_agent_config(self, chat_id: int | str | None = None) -> dict[str, Any]:
        # Keep thread_id request-scoped to avoid shared mutable config across concurrent calls.
        return {
            "configurable": {
                "thread_id": self._thread_id(chat_id),
            }
        }

    def resolve_model_name(self, model_name: str) -> str:
        requested = (model_name or "").strip().casefold()
        if requested in LLM_SERVICE_PROVIDERS:
            return LLM_SERVICE_PROVIDERS[requested]

        available_values = set(LLM_SERVICE_PROVIDERS.values())
        if model_name in available_values:
            return model_name

        available = ", ".join(sorted(LLM_SERVICE_PROVIDERS.keys()))
        raise ValueError(f"Unknown model '{model_name}'. Available: {available}")

    def set_active_model(self, model: str = "light", chat_id: int | str | None = None) -> str:
        resolved_model = self.resolve_model_name(model)
        # Rebuild the single agent only when model actually changes.
        if resolved_model != self.active_model:
            self.active_model = resolved_model
            self.agent = self._init_agent(model=resolved_model)
        return resolved_model

    def get_active_model(self, chat_id: int | str | None = None) -> str:
        return self.active_model

    def call_agent(self, prompt: str, chat_id: int | str | None = None) -> str:
        agent_config = self._build_agent_config(chat_id=chat_id)

        try:
            response = self.agent.invoke(
                {"messages": [HumanMessage(content=prompt)]},
                config=agent_config,
            )
        except Exception as exc:
            return f"error executing agent: {exc}"

        message = response["messages"][-1]
        content = getattr(message, "content", "")

        if isinstance(content, str):
            return content

        if isinstance(content, list):
            text_parts: list[str] = []
            for item in content:
                if isinstance(item, dict) and item.get("type") == "text":
                    text_parts.append(str(item.get("text", "")))
                elif isinstance(item, str):
                    text_parts.append(item)
            joined = "".join(text_parts).strip()
            if joined:
                return joined

        return str(content)


_LLM_SERVICE = LLMService()


def get_llm_service() -> LLMService:
    return _LLM_SERVICE


def resolve_model_name(model_name: str) -> str:
    return _LLM_SERVICE.resolve_model_name(model_name)


def set_active_model(model_name: str) -> str:
    return _LLM_SERVICE.set_active_model(model_name)


def get_active_model() -> str:
    return _LLM_SERVICE.get_active_model()


def generate_response(prompt: str, chat_id: int | str) -> str:
    return _LLM_SERVICE.call_agent(prompt, chat_id=chat_id)