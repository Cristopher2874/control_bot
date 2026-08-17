from __future__ import annotations

from telegram import Update
from telegram.ext import ContextTypes

import config
from features.student_tools import (
    open_student_browser,
    open_student_calculator,
    open_student_notes,
)
from llm_service import get_active_model, set_active_model


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    active_model = get_active_model(chat_id)
    available = ", ".join(sorted(config.AVAILABLE_MODELS.keys()))
    await update.message.reply_text(
        f"System online! This chat is currently using {active_model}. "
        f"To switch models, send /model gemma or /model light. Available: {available}. "
        "Quick student tools: /notes, /browser, /calculator."
    )


async def set_model_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    args = context.args

    if not args:
        available = ", ".join(sorted(config.AVAILABLE_MODELS.keys()))
        current = get_active_model(chat_id)
        await update.message.reply_text(
            f"Current model for this chat: {current}. Available: {available}. "
            "Usage: /model gemma or /model light"
        )
        return

    requested = " ".join(args)
    try:
        resolved = set_active_model(chat_id, requested)
        await update.message.reply_text(
            f"✅ Model updated for this chat: {resolved}. "
            "Send your next message and it will use this model."
        )
    except ValueError as exc:
        await update.message.reply_text(str(exc))


async def open_notes_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📒 Opening your student notes file...")
    open_student_notes()


async def open_browser_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🌐 Opening browser for quick research...")
    open_student_browser()


async def open_calculator_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🧮 Opening calculator...")
    open_student_calculator()


async def list_models_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    available = ", ".join(sorted(config.AVAILABLE_MODELS.keys()))
    current = get_active_model(update.effective_chat.id)
    await update.message.reply_text(f"Current model: {current}. Available: {available}")


async def reset_chat_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # This is a placeholder for the future memory-reset logic.
    await update.message.reply_text(
        "🧹 Conversation reset hook ready. This will clear the current chat context once the memory store is added."
    )
