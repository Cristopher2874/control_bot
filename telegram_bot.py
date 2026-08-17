# telegram_bot.py
import asyncio

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

import config
from bot_commands import (
    list_models_command,
    open_browser_command,
    open_calculator_command,
    open_notes_command,
    set_model_command,
    start,
)
from llm_service import generate_response, get_active_model, set_active_model


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text or ""
    text = user_text.strip()
    chat_id = update.effective_chat.id

    if not text:
        return

    command = text.lower()
    if command.startswith("/model") or command.startswith("/setmodel") or command.startswith("model ") or command.startswith("set model "):
        model_name = text.split(maxsplit=1)[1] if " " in text else ""
        requested = model_name.strip()
        try:
            resolved = set_active_model(chat_id, requested)
            await update.message.reply_text(
                f"✅ Model updated for this chat: {resolved}. "
                "Your next message will use this model."
            )
        except ValueError as exc:
            await update.message.reply_text(str(exc))
        return

    if command in {"/models", "/listmodels", "models", "list models"}:
        await list_models_command(update, context)
        return

    if command in {"/notes", "/notebook", "/opennotes"}:
        await open_notes_command(update, context)
        return

    if command in {"/browser", "/openbrowser", "/research"}:
        await open_browser_command(update, context)
        return

    if command in {"/calculator", "/calc", "/math"}:
        await open_calculator_command(update, context)
        return

    print(f"\n[*] Received prompt: {user_text}")
    status_msg = await update.message.reply_text("⏳ Request received. Initializing agent...")

    try:
        active_model = get_active_model(chat_id)
        print(f"[*] Sending to {active_model} for chat {chat_id}...")

        loop = asyncio.get_running_loop()
        response_text = await loop.run_in_executor(None, generate_response, user_text, chat_id)

        await status_msg.edit_text(response_text)
        print("[*] Success! Response sent.")

    except Exception as e:
        error_msg = f"❌ Error during execution:\n{str(e)}\n\nCheck if Ollama is running and the model is pulled."
        await status_msg.edit_text(error_msg)
        print(f"[*] Error: {str(e)}")


def run_bot():
    print("Starting the Telegram listener...")
    app = ApplicationBuilder().token(config.BOT_TOKEN).build()

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