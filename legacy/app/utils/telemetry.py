import logging
import sys
import threading
import time
import psutil
import re
from datetime import datetime
from typing import Callable

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


class SensitiveDataFilter(logging.Filter):
    """Masks sensitive data like API keys and tokens in log messages."""
    
    def __init__(self, name=""):
        super().__init__(name)
        # Patterns for secrets
        self.sensitive_patterns = [
            re.compile(r'\d{9,10}:[a-zA-Z0-9_-]{35}'),  # Telegram Bot Token
            re.compile(r'(?i)api_key[\s=:]+[a-zA-Z0-9_-]+'), # API Key variants
            re.compile(r'(?i)bearer[\s=:]+[a-zA-Z0-9_\-\.]+'), # Bearer tokens
            re.compile(r'(?i)secret[\s=:]+[a-zA-Z0-9_\-\.]+'), # Generic secrets
        ]

    def filter(self, record: logging.LogRecord) -> bool:
        # Sanitize the main log message string
        if isinstance(record.msg, str):
            for pattern in self.sensitive_patterns:
                record.msg = pattern.sub('***REDACTED***', record.msg)
                
        # Sanitize any string arguments passed to the logger
        if isinstance(record.args, tuple) and record.args:
            safe_args = []
            for arg in record.args:
                if isinstance(arg, str):
                    for pattern in self.sensitive_patterns:
                        arg = pattern.sub('***REDACTED***', arg)
                safe_args.append(arg)
            record.args = tuple(safe_args)
            
        return True

class ModuleAllowListFilter(logging.Filter):
    """
    Blocks all logs except those originating from the allowed module prefixes.
    This safely ignores noisy or sensitive third-party logs (like telegram or httpcore).
    """
    def __init__(self, allowed_prefixes: List[str]):
        super().__init__()
        # Convert to tuple for use with string.startswith()
        self.allowed_prefixes = tuple(allowed_prefixes)

    def filter(self, record: logging.LogRecord) -> bool:
        # Check if the logger's name starts with any of our allowed prefixes
        return record.name.startswith(self.allowed_prefixes)


def setup_logging(log_file: str = "app_debug.log") -> None:
    """Configures root logger with console and file handlers."""
    root_logger_level = GlobalConfigProvider().get_config_value("telemetry", "logger_level", "INFO")

    root_logger = logging.getLogger()
    
    if isinstance(root_logger_level, str):
        level_value = getattr(logging, root_logger_level.upper(), logging.INFO)
        root_logger.setLevel(level_value)
    else:
        root_logger.setLevel(root_logger_level)

    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    formatter = logging.Formatter(
        '%(asctime)s : %(levelname)s : %(name)s'
        ' : trace_id : %(trace_id)s : chat_id : %(chat_id)s : %(message)s'
    )

    trusted_modules = GlobalConfigProvider().get_list("telemetry","trusted_modules", [])
    
    # 2. Instantiate all filters
    context_filter = ContextFilter()
    sensitive_filter = SensitiveDataFilter()
    allowlist_filter = ModuleAllowListFilter(trusted_modules)

    # 3. Console Handler attachments
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.addFilter(allowlist_filter)  # Block unwanted modules first
    console_handler.addFilter(context_filter)    # Inject trace/chat IDs
    console_handler.addFilter(sensitive_filter)  # Mask any secrets in allowed logs
    console_handler.setFormatter(formatter)

    # 4. File Handler attachments
    file_handler = logging.FileHandler(log_file)
    file_handler.addFilter(allowlist_filter)     # Block unwanted modules first
    file_handler.addFilter(context_filter)       # Inject trace/chat IDs
    file_handler.addFilter(sensitive_filter)     # Mask any secrets in allowed logs
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

def monitor_ollama_process(interval=1) -> Callable[[], None]:
    """Start Ollama monitoring and return a function that stops it."""
    system_logs_active = GlobalConfigProvider().get_bool("telemetry", "system_logs", False)
    logger = logging.getLogger("System logs tracing")
    stop_event = threading.Event()

    if not system_logs_active:
        logger.info("Hardware logs disabled")
        return stop_event.set

    def monitor() -> None:
        logger.info("Hardware logs active")
        try:
            ollama_process = next(
                (
                    proc
                    for proc in psutil.process_iter(["pid", "name"])
                    if "ollama" in (proc.info.get("name") or "").lower()
                ),
                None,
            )
            if not ollama_process:
                logger.info("Ollama process not found")
                return

            logger.info("Found Ollama process: PID %s", ollama_process.pid)
            while not stop_event.is_set():
                metrics = get_system_metrics()
                try:
                    process = psutil.Process(ollama_process.pid)
                    metrics["ollama_cpu_percent"] = process.cpu_percent(interval=0.1)
                    metrics["ollama_ram_mb"] = process.memory_info().rss / (1024 ** 2)
                    metrics["ollama_num_threads"] = process.num_threads()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass

                logger.info(
                    " : cpu_percent=%.1f, ram_percent=%.1f, "
                    "ram_mb=%.1f, ram_total_mb=%.1f, ollama_cpu_percent=%s, "
                    "ollama_ram_mb=%s, ollama_num_threads=%s",
                    metrics["cpu_percent"],
                    metrics["ram_percent"],
                    metrics["ram_mb"],
                    metrics["ram_total_mb"],
                    metrics.get("ollama_cpu_percent", "N/A"),
                    metrics.get("ollama_ram_mb", "N/A"),
                    metrics.get("ollama_num_threads", "N/A"),
                )
                stop_event.wait(interval)
        except Exception:
            logger.exception("Monitoring error")
        finally:
            logger.info("Hardware monitoring complete")

    monitor_thread = threading.Thread(target=monitor, name="ollama-monitor", daemon=True)
    monitor_thread.start()

    def stop_monitor() -> None:
        stop_event.set()
        monitor_thread.join()

    return stop_monitor