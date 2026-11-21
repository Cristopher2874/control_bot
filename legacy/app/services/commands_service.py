import os
import subprocess
import webbrowser
from pathlib import Path

from telegram import Update
from telegram.ext import ContextTypes

from app.config.llm_service_providers import LLM_SERVICE_PROVIDERS
from app.services.llm_service import get_llm_service

LLM_SERVICE = get_llm_service()


def _available_models_text() -> str:
    entries = [f"- {alias}: {model}" for alias, model in sorted(LLM_SERVICE_PROVIDERS.items())]
    return "\n".join(entries)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    active_model = LLM_SERVICE.get_active_model()
    await update.message.reply_text(
        "System online.\n"
        f"Active model for this chat: {active_model}\n\n"
        "Available aliases:\n"
        f"{_available_models_text()}\n\n"
        "Commands: /model, /models, /notes, /browser, /calculator, /stop"
    )


async def list_models_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    current = LLM_SERVICE.get_active_model()
    await update.message.reply_text(
        "Available models:\n"
        f"{_available_models_text()}\n\n"
        f"Current model for this chat: {current}"
    )


async def set_model_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args

    if not args:
        current = LLM_SERVICE.get_active_model()
        await update.message.reply_text(
            "Usage: /model <alias-or-model-name>\n"
            f"Current model: {current}\n\n"
            "Available aliases:\n"
            f"{_available_models_text()}"
        )
        return

    requested = " ".join(args)
    try:
        resolved = LLM_SERVICE.set_active_model(requested)
    except ValueError as exc:
        await update.message.reply_text(str(exc))
        return

    await update.message.reply_text(
        f"Model updated for this chat: {resolved}."
    )


async def open_notes_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        notes_path = Path.home() / "Documents" / "pei_notes.txt"
        notes_path.parent.mkdir(parents=True, exist_ok=True)
        if not notes_path.exists():
            notes_path.write_text("PEI Notes\n\n", encoding="utf-8")

        if os.name == "nt":
            os.startfile(str(notes_path))
        else:
            subprocess.Popen(["xdg-open", str(notes_path)])
        await update.message.reply_text(f"Opened notes file: {notes_path}")
    except Exception as exc:
        await update.message.reply_text(f"Could not open notes: {exc}")


async def open_browser_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        webbrowser.open("https://www.google.com")
        await update.message.reply_text("Opened your browser for research.")
    except Exception as exc:
        await update.message.reply_text(f"Could not open browser: {exc}")


async def open_calculator_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if os.name == "nt":
            subprocess.Popen(["calc.exe"])
        else:
            webbrowser.open("https://www.google.com/search?q=calculator")
        await update.message.reply_text("Opened calculator.")
    except Exception as exc:
        await update.message.reply_text(f"Could not open calculator: {exc}")


async def stop_bot_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text("Stopping bot listener. You can start it again from the terminal.")

    print("[*] Stop command received. Shutting down polling...")
    context.application.stop_running()