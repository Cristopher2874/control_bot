import logging
import time
from typing import Any, Dict, List
from langchain_core.callbacks import BaseCallbackHandler


class AgentLoggingHandler(BaseCallbackHandler):
    """LangChain callback handler to capture token usage and timing metrics."""

    def __init__(self):
        self.logger = logging.getLogger("LLMService.Callback")
        self.start_time = None

    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> None:
        self.start_time = time.perf_counter()
        self.logger.info(f"[LLM_CALL_START] prompt_count={len(prompts)}")

    def on_llm_end(self, response: Any, **kwargs: Any) -> None:
        duration = (
            time.perf_counter() - self.start_time
            if self.start_time
            else 0.0
        )
        token_usage = (
            response.llm_output.get("token_usage", {})
            if response.llm_output
            else {}
        )

        prompt_tokens = token_usage.get("prompt_tokens", "N/A")
        completion_tokens = token_usage.get("completion_tokens", "N/A")
        total_tokens = token_usage.get("total_tokens", "N/A")

        self.logger.info(
            f"[LLM_CALL_SUCCESS] duration={duration:.2f}s, "
            f"prompt_tokens={prompt_tokens}, completion_tokens={completion_tokens}, "
            f"total_tokens={total_tokens}"
        )

    def on_llm_error(self, error: Exception, **kwargs: Any) -> None:
        duration = (
            time.perf_counter() - self.start_time
            if self.start_time
            else 0.0
        )
        self.logger.error(
            f"[LLM_CALL_ERROR] duration={duration:.2f}s, error={error}"
        )