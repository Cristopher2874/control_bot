import asyncio

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

from config.global_config import GlobalConfigProvider
from bot_commands import (
    list_models_command,
    open_browser_command,
    open_calculator_command,
    open_notes_command,
    set_model_command,
    start,
)
from utils import markdown_to_telegram_html


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text or ""
    text = user_text.strip()
    chat_id = update.effective_chat.id

    if not text:
        return

    print(f"\n[*] Received prompt: {user_text}")
    status_msg = await update.message.reply_text("⏳ Request received. Initializing agent...")

    try:
        active_model = get_active_model(chat_id)
        print(f"[*] Sending to {active_model} for chat {chat_id}...")

        loop = asyncio.get_running_loop()
        response_text = await loop.run_in_executor(None, generate_response, user_text, chat_id)
        formatted_text = markdown_to_telegram_html(response_text)

        await status_msg.edit_text(formatted_text, parse_mode=ParseMode.HTML)
        print("[*] Success! Response sent.")

    except Exception as e:
        error_msg = f"❌ Error during execution:\n{str(e)}\n\nCheck if Ollama is running and the model is pulled."
        await status_msg.edit_text(error_msg)
        print(f"[*] Error: {str(e)}")


def run_bot():
    print("Starting the Telegram listener...")
    config = GlobalConfigProvider()
    app = ApplicationBuilder().token(config.get_config_value("telegram","bot_sk_token","")).build()

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
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is polling. Send a message from your phone!")
    app.run_polling()