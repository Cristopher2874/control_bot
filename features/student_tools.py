import os
import subprocess
import webbrowser
from pathlib import Path


def open_student_notes():
    """Open a local notes file for student use."""
    notes_path = Path(__file__).resolve().parents[1] / "student_notes.txt"
    notes_path.parent.mkdir(parents=True, exist_ok=True)
    if not notes_path.exists():
        notes_path.write_text(
            "Student Notes\n===============\n\n- Topic:\n- Summary:\n- To-do:\n",
            encoding="utf-8",
        )

    if os.name == "nt":
        os.startfile(str(notes_path))
    else:
        subprocess.Popen(["xdg-open", str(notes_path)])


def open_student_browser():
    """Open the default browser for quick research."""
    webbrowser.open("https://www.google.com")


def open_student_calculator():
    """Open the system calculator."""
    if os.name == "nt":
        subprocess.Popen(["calc.exe"])
    else:
        subprocess.Popen(["open", "/Applications/Calculator.app"])
