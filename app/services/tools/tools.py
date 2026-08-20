import webbrowser
import time
import pyautogui
from langchain_core.tools import tool

@tool
def open_gemini_in_chrome() -> str:
    """Opens Google Gemini in a new Google Chrome tab."""
    try:
        # Opens Gemini in your default browser or explicitly via Chrome
        gemini_url = "https://gemini.google.com"

        webbrowser.open(gemini_url)
        
        return "Successfully opened Gemini on Chrome."
    except Exception as e:
        return f"Failed to open Gemini: {str(e)}"

@tool
def prompt_claude_desktop(prompt_text: str) -> str:
    """Launches Claude Desktop, waits for it to load, types a prompt, and submits it."""
    try:
        # Windows key is named "win" in PyAutoGUI.
        # Win+S opens the Windows Search box, which is the right way to start searching.
        pyautogui.hotkey('win', 's')
        time.sleep(1.5)
        pyautogui.write("claude", interval=0.01)
        time.sleep(0.5)
        pyautogui.press('enter')

        # Wait for the window to open/focus.
        time.sleep(10)

        # Type the prompt and submit it.
        pyautogui.write(prompt_text, interval=0.01)
        pyautogui.press('enter')

        return f"Prompt typed into Claude Desktop: '{prompt_text}'"
    except Exception as e:
        return f"GUI Automation failed: {str(e)}"

TOOLS = [prompt_claude_desktop, open_gemini_in_chrome]