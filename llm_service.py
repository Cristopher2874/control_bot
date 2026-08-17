# llm_service.py
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
import config

# Initialize the LangChain Ollama model
llm = ChatOllama(
    model=config.OLLAMA_MODEL,
    base_url=config.OLLAMA_BASE_URL,
    temperature=0.7
)

def generate_response(prompt: str) -> str:
    """
    Sends the prompt to local Ollama and returns the response.
    Includes error handling to catch execution failures.
    """
    try:
        # We start with a simple HumanMessage. 
        # When you upgrade to LangGraph, you will invoke your compiled graph here instead.
        messages = [HumanMessage(content=prompt)]
        response = llm.invoke(messages)
        return response.content
    except Exception as e:
        # This catches issues like Ollama being turned off or the model not existing
        raise RuntimeError(f"LLM Execution Failed: {str(e)}")

if __name__ == "__main__":
    response = generate_response("Hello! What's the capital of France")
    print(response)