from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="ollama:gemma4:e2b",
    tools=[get_weather],
    system_prompt="You are a helpful assistant. Be concise with responses",
    checkpointer=InMemorySaver()
)

config = {"configurable": {"thread_id":"1"}}

result = agent.invoke(
    {"messages": [HumanMessage("Use the tool and tell me what's the weather on SF.")]},
    config=config
)
print(result["messages"][-1].content_blocks)