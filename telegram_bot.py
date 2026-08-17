# telegram_bot.py
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import config
from llm_service import generate_response

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"System online! Send a prompt to run on {config.OLLAMA_MODEL}.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    print(f"\n[*] Received prompt: {user_text}")
    
    # 1. Send immediate confirmation so you know the PC received it
    status_msg = await update.message.reply_text("⏳ Request received. Initializing agent...")

    try:
        print(f"[*] Sending to {config.OLLAMA_MODEL}...")
        
        # 2. Run the LLM in a background thread to keep the bot responsive
        loop = asyncio.get_running_loop()
        response_text = await loop.run_in_executor(None, generate_response, user_text)
        
        # 3. Edit the confirmation message with the final AI response
        await status_msg.edit_text(response_text)
        print("[*] Success! Response sent.")
        
    except Exception as e:
        # 4. If something fails, update the message with the error log
        error_msg = f"❌ Error during execution:\n{str(e)}\n\nCheck if Ollama is running and the model is pulled."
        await status_msg.edit_text(error_msg)
        print(f"[*] Error: {str(e)}")

def run_bot():
    print("Starting the Telegram listener...")
    app = ApplicationBuilder().token(config.BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is polling. Send a message from your phone!")
    app.run_polling()