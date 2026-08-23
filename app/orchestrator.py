import asyncio
import logging
import uuid

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

from app.utils.telemetry import setup_logging, trace_id_var, chat_id_var
from app.config.global_config import GlobalConfigProvider
from app.services.commands_service import (
    list_models_command,
    open_browser_command,
    open_calculator_command,
    open_notes_command,
    set_model_command,
    stop_bot_command,
    start,
)
from app.services.llm_service import get_llm_service
from app.services.llm_router import get_llm_router
from app.utils import markdown_to_telegram_html

LLM_SERVICE = get_llm_service()
LLM_ROUTER = get_llm_router()
setup_logging()
logger = logging.getLogger("Orchestrator")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    user_text = update.message.text or ""
    text = user_text.strip()
    chat_id = update.effective_chat.id

    if not text:
        return

    print(f"\n[*] Received prompt: {user_text}")
    status_msg = await update.message.reply_text("⏳ Request received. Initializing agent...")

    try:
        loop = asyncio.get_running_loop()
        response_text = await loop.run_in_executor(None, LLM_ROUTER.run_agent, user_text, chat_id)
        formatted_text = markdown_to_telegram_html(response_text)

        await status_msg.edit_text(formatted_text, parse_mode=ParseMode.HTML)

    except Exception as e:
        error_msg = f"❌ Error during execution:\n{str(e)}\n\nCheck if Ollama is running and the model is pulled."
        await status_msg.edit_text(error_msg)
        logger.error(f"[*] Error: {str(e)}")


def run_bot():
    trace_id_var.set(str(uuid.uuid4()))
    chat_id_var.set(trace_id_var)
    logger.info("Starting the listener...")
    config = GlobalConfigProvider()
    app = ApplicationBuilder().token(config.get_config_value("telegram", "bot_sk_token", "")).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("model", set_model_command))
    app.add_handler(CommandHandler("setmodel", set_model_command))
    app.add_handler(CommandHandler("models", list_models_command))
    app.add_handler(CommandHandler("notes", open_notes_command))
    app.add_handler(CommandHandler("notebook", open_notes_command))
    app.add_handler(CommandHandler("browser", open_browser_command))
    app.add_handler(CommandHandler("research", open_browser_command))
    app.add_handler(CommandHandler("calculator", open_calculator_command))
    app.add_handler(CommandHandler("calc", open_calculator_command))
    app.add_handler(CommandHandler("stop", stop_bot_command))
    app.add_handler(CommandHandler("shutdown", stop_bot_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("App ready to poll")
    app.run_polling()