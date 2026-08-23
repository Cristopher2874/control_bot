import logging
import sys
import time
import psutil
import time
from datetime import datetime
import json

from contextvars import ContextVar
from typing import Any, Dict, List
from langchain_core.callbacks import BaseCallbackHandler

from app.config.global_config import GlobalConfigProvider

# Context variables accessible across async/sync execution paths
trace_id_var: ContextVar[str | None] = ContextVar("trace_id", default=None)
chat_id_var: ContextVar[str | int | None] = ContextVar("chat_id", default=None)


class ContextFilter(logging.Filter):
    """Injects current context variables into every LogRecord."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.trace_id = trace_id_var.get() or "N/A"
        record.chat_id = chat_id_var.get() or "N/A"
        return True


def setup_logging(log_file: str = "app_debug.log") -> None:
    """Configures root logger with JSON-formatted console and file handlers."""
    root_logger_level = GlobalConfigProvider().get_config_value("telemetry", "logger_level", "INFO")

    root_logger = logging.getLogger()
    root_logger.setLevel(root_logger_level)

    # Avoid adding duplicate handlers if re-initialized
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    # Formatter outputting structured JSON
    formatter = logging.Formatter(
        '{"time": "%(asctime)s", "level": "%(levelname)s", "module": "%(name)s", '
        '"trace_id": "%(trace_id)s", "chat_id": "%(chat_id)s", "message": "%(message)s"}'
    )

    context_filter = ContextFilter()

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.addFilter(context_filter)
    console_handler.setFormatter(formatter)

    # File Handler
    file_handler = logging.FileHandler(log_file)
    file_handler.addFilter(context_filter)
    file_handler.setFormatter(formatter)

    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

"""
LLM metrics usage
"""

class AgentLoggingHandler(BaseCallbackHandler):
    """LangChain callback handler to capture token usage and timing metrics."""

    def __init__(self):
        self.logger = logging.getLogger("LLMService.Callback")
        self.start_time = None

    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> None:
        self.start_time = time.perf_counter()
        self.logger.info(f"LLM call starts, prompt_count={len(prompts)}")

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
            f"model done duration={duration:.2f}s, "
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
            f"model error, duration={duration:.2f}s, error={error}"
        )

"""
Hardware usage
"""

def get_system_metrics():
    """Capture CPU, RAM, GPU usage"""
    metrics = {
        "timestamp": datetime.now().isoformat(),
        "cpu_percent": psutil.cpu_percent(interval=0.5),
        "ram_percent": psutil.virtual_memory().percent,
        "ram_mb": psutil.virtual_memory().used / (1024 ** 2),
        "ram_total_mb": psutil.virtual_memory().total / (1024 ** 2),
    }
    return metrics

def monitor_ollama_process(duration_seconds=300, interval=1):
    """Monitor Ollama process for N seconds"""
    system_logs_active = GlobalConfigProvider().get_config_value("telemetry", "system_logs", "False")
    logger = logging.getLogger("System logs tracing")

    if system_logs_active:
        logger.info("Hardware logs active")
        try:
            # Find Ollama process
            ollama_process = None
            for proc in psutil.process_iter(['pid', 'name']):
                if 'ollama' in proc.name().lower():
                    ollama_process = proc
                    logger.info(f"Found Ollama process: PID {proc.pid}")
                    break
            
            if not ollama_process:
                logger.info("Ollama process not found!")
                return
            
            log_file = open('ollama_monitor.jsonl', 'a')
            start_time = time.time()
            
            while time.time() - start_time < duration_seconds:
                metrics = get_system_metrics()
                
                # Add process-specific metrics
                try:
                    proc = psutil.Process(ollama_process.pid)
                    metrics['ollama_cpu_percent'] = proc.cpu_percent(interval=0.1)
                    metrics['ollama_ram_mb'] = proc.memory_info().rss / (1024 ** 2)
                    metrics['ollama_num_threads'] = proc.num_threads()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
                
                # Log to JSONL (one JSON per line, easy to parse later)
                log_file.write(json.dumps(metrics) + '\n')
                log_file.flush()
                
                # logger.info to console
                logger.info(f"RAM: {metrics['ram_percent']:.1f}% | "
                    f"CPU: {metrics['cpu_percent']:.1f}% | "
                    f"Ollama RAM: {metrics.get('ollama_ram_mb', 'N/A'):.0f}MB")
                
                time.sleep(interval)
            
            log_file.close()
            logger.info(f"Monitoring complete. Logs saved to ollama_monitor.jsonl")
    
        except Exception as e:
            logger.info(f"Monitoring error: {e}")

    else:
        logger.info("Hardware logs disabled")
