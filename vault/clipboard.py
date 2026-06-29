"""Clipboard management for macOS."""

import subprocess
import threading
import time

def copy_to_clipboard(text: str):
    """
    Copies text to the clipboard.

    Args:
        text: The text to copy.
    """
    subprocess.run("pbcopy", input=text.encode("utf-8"), check=True)

def clear_clipboard_after(delay: int):
    """
    Clears the clipboard after a delay.

    Args:
        delay: The delay in seconds.
    """
    def _clear():
        time.sleep(delay)
        # Clear clipboard by copying an empty string
        subprocess.run("pbcopy", input="".encode("utf-8"), check=True)

    thread = threading.Thread(target=_clear)
    thread.daemon = True
    thread.start()
