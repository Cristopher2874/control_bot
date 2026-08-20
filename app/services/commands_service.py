from telegram import Update
from telegram.ext import ContextTypes

from services.llm_service import LLMService
from config.llm_service_providers import LLM_SERVICE_PROVIDERS

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    active_model = LLMService().get_active_model()
    available = ", ".join(sorted(LLM_SERVICE_PROVIDERS.keys()))
    await update.message.reply_text(
        f"System online! This chat is currently using {active_model}. "
        f"To switch models, send /model gemma or /model light. Available: {available}. "
        "Quick student tools: /notes, /browser, /calculator."
    )

async def set_model_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    args = context.args

    if not args:
        available = ", ".join(sorted(LLM_SERVICE_PROVIDERS.keys()))
        current = LLMService().get_active_model()
        await update.message.reply_text(
            f"Current model for this chat: {current}. Available: {available}. "
            "Usage: /model gemma or /model light"
        )
        return

    requested = " ".join(args)
    try:
        resolved = LLMService().set_active_model(requested)
        await update.message.reply_text(
            f"✅ Model updated for this chat: {resolved}. "
            "Send your next message and it will use this model."
        )
    except ValueError as exc:
        await update.message.reply_text(str(exc))