# PEI Control Bot

A Telegram productivity assistant with a local Ollama LLM backend and command-first student utilities.

## Quick start

1. Install dependencies.
2. Make sure Ollama is running locally.
3. Add your Telegram bot token in the environment.
4. Run the app with:

   python main.py

## Command documentation

The feature registry is available in [docs/FEATURES.md](docs/FEATURES.md).

## Core features

- model switching per chat
- command-only productivity actions
- local student tools: notes, browser, calculator
- extensible modular command structure

## Architecture

- `config.py` — environment and model configuration
- `llm_service.py` — LLM access and model resolution
- `bot_commands.py` — command handlers
- `features/` — feature modules for local tools
- `telegram_bot.py` — thin Telegram router
