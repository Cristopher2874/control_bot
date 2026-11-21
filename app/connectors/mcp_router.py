from PIL import ImageCms
from langsmith._openapi_client.types import run_select_field
import asyncio
from typing import Any, List
from pydantic import BaseModel

from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.checkpoint.memory import InMemorySaver

# Model providers mapping shaped like app.config.llm_service_providers
DEFAULT_PROVIDERS = {
    "light": "gemma4:e2b",
    "standard": "gemma4:e4b",
    "fast": "llama3.1:8b",
    "cloud": "gemma4:31b-cloud",
}

try:
    from app.config.llm_service_providers import LLM_SERVICE_PROVIDERS
except ImportError:
    LLM_SERVICE_PROVIDERS = DEFAULT_PROVIDERS

WEATHER_SYSTEM_PROMPT = (
    "You are a helpful and knowledgeable weather assistant. "
    "You have access to tools that fetch live weather data and multi-day forecasts. "
    "Always invoke the appropriate weather tool when the user asks for weather conditions or forecasts, "
    "and present the results in a friendly, well-formatted response."
)

class MCPRouter:
    def __init__(self, mcp_client_list):
        self.mcp_router_main_client = MultiServerMCPClient(mcp_client_list)
        self.tools


class WeatherLLMClient:
    """Weather Client that connects to the Weather MCP HTTP server

    and uses a local Ollama model shaped after app.services.llm_service.
    """

    def __init__(
        self,
        server_url: str = "http://127.0.0.1:8000/mcp",
        default_model_alias: str = "fast",
    ):
        self.server_url = server_url
        self.checkpointer = InMemorySaver()
        self.default_model = self.resolve_model_name(default_model_alias)
        self.active_model = self.default_model
        self.mcp_client = MultiServerMCPClient(
            {
                "weather": {
                    "transport": "http",
                    "url": self.server_url,
                }
            }
        )
        self.tools: list[Any] = []
        self.agent: Any = None

    def resolve_model_name(self, model_name: str) -> str:
        requested = (model_name or "").strip().casefold()
        if requested in LLM_SERVICE_PROVIDERS:
            return LLM_SERVICE_PROVIDERS[requested]

        available_values = set(LLM_SERVICE_PROVIDERS.values())
        if model_name in available_values:
            return model_name

        available = ", ".join(sorted(LLM_SERVICE_PROVIDERS.keys()))
        raise ValueError(f"Unknown model '{model_name}'. Available: {available}")

    def _thread_id(self, chat_id: int | str | None = None) -> str:
        if chat_id is None:
            return "weather-user-default"
        return str(chat_id)

    async def initialize(self) -> None:
        """Fetch MCP tools from the HTTP server and compile the LangChain agent."""
        logger.info("Connecting to Weather MCP server and fetching tools...")
        self.tools = await self.mcp_client.get_tools()
        logger.info("Loaded %d tool(s) from Weather MCP: %s", len(self.tools), [t.name for t in self.tools])
        self.agent = self._init_agent(model=self.active_model)

    def _init_agent(self, model: str) -> Any:
        provider_model = model if model.startswith("ollama:") else f"ollama:{model}"
        logger.info("Compiling LangChain/LangGraph agent with model: %s", provider_model)
        return create_agent(
            model=provider_model,
            tools=self.tools,
            system_prompt=WEATHER_SYSTEM_PROMPT,
            checkpointer=self.checkpointer,
        )

    def _build_agent_config(self, chat_id: int | str | None = None) -> dict[str, Any]:
        return {
            "configurable": {
                "thread_id": self._thread_id(chat_id),
            }
        }

    async def acall_agent(self, prompt: str, chat_id: int | str | None = None) -> str:
        """Asynchronously send a prompt to the agent and return formatted response."""
        if self.agent is None:
            await self.initialize()

        agent_config = self._build_agent_config(chat_id=chat_id)
        logger.debug("Calling agent with prompt: %s", prompt)

        try:
            response = await self.agent.ainvoke(
                {"messages": [HumanMessage(content=prompt)]},
                config=agent_config,
            )
        except Exception as exc:
            logger.error("Error executing agent: %s", exc)
            return f"Error executing agent: {exc}"

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


async def main():
    print("=== Weather MCP LangChain Client Demo ===")
    client = WeatherLLMClient(
        server_url="http://127.0.0.1:8000/mcp",
        default_model_alias="fast",  # resolves to llama3.1:8b (ollama:llama3.1:8b)
    )

    try:
        await client.initialize()
    except Exception as e:
        print(f"\n[!] Failed to connect to Weather MCP server at {client.server_url}.")
        print("Please ensure the weather server is running first:")
        print("  python mcps/weather/server.py")
        print(f"\nDetails: {e}")
        return

    queries = [
        "What is the current weather in Tokyo?",
        "Can you give me a 3-day forecast for London?",
    ]

    for q in queries:
        print(f"\nUser: {q}")
        reply = await client.acall_agent(q)
        print(f"Assistant: {reply}")


if __name__ == "__main__":
    asyncio.run(main())
