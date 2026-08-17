# Bot Features and Commands

This project is designed as a Telegram productivity assistant with a local Ollama LLM backend.

## Command design

The bot is structured around a command-first model:

- direct commands execute locally without LLM access
- plain-text messages can be sent to the Ollama model
- model selection and conversation memory remain independent per chat

## Available commands

### Core model controls
- `/start` — shows bot status and active model
- `/model <name>` — change the active model for the current chat
- `/models` — list available models

### Student tools
- `/notes` — open a local notes file
- `/browser` — open the default browser for research
- `/calculator` — open the system calculator

### Conversation controls
- `/reset` — clear the current chat memory
- `/newchat` — start a fresh chat context

## Recommended architecture

The app should stay modular:

- `config.py` for environment and defaults
- `llm_service.py` for model resolution and LLM calls
- `features/` for command-specific local tools
- `telegram_bot.py` for Telegram wiring only

## Example usage

- `/model light`
- `/notes`
- `/browser`
- `/calculator`
- `/newchat`
- `/model heavy`

## Scalability notes

Keep the Telegram bot file thin. It should route commands to feature handlers, not contain all business logic in one place.
