"""Formatting helpers for rendering model output in Telegram-safe formats."""

from .telegram_markdown import markdown_to_telegram_html

__all__ = ["markdown_to_telegram_html"]
