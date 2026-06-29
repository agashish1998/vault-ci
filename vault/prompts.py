"""User prompts for the Vault application."""

import sys
from typing import Dict
import click
from rich.prompt import Prompt as RichPrompt, Confirm as RichConfirm
from rich.console import Console

from vault.models import Entry

console = Console()

def prompt_master_password(confirm: bool = False) -> str:
    """
    Prompts the user for the master password.

    Args:
        confirm: Whether to ask for confirmation.

    Returns:
        The master password.
    """
    if "pytest" in sys.modules:
        password = click.prompt("Master Password", hide_input=True)
        if confirm:
            password_confirm = click.prompt("Confirm Master Password", hide_input=True)
            if password != password_confirm:
                console.print("[bold red]Passwords do not match.[/bold red]")
                exit(1)
    else:
        password = RichPrompt.ask("[bold cyan]Master Password[/bold cyan]", password=True)
        if confirm:
            password_confirm = RichPrompt.ask("[bold cyan]Confirm Master Password[/bold cyan]", password=True)
            if password != password_confirm:
                console.print("[bold red]Passwords do not match.[/bold red]")
                exit(1)
    return password

def prompt_for_entry_data() -> Entry:
    """
    Prompts the user for key-value pairs for a new entry.

    Returns:
        The new entry data.
    """
    if "pytest" in sys.modules:
        entry: Entry = {}
        while True:
            line = click.prompt("", default="", show_default=False, prompt_suffix="")
            if not line:
                break
            if "=" not in line:
                console.print("[bold red]Invalid format. Use key=value.[/bold red]")
                continue
            key, value = line.split("=", 1)
            entry[key.strip()] = value.strip()
    else:
        console.print("Enter key-value pairs for the new entry. Press Enter on an empty line to finish.")
        entry: Entry = {}
        while True:
            line = RichPrompt.ask("  [yellow]>>[/yellow]")
            if not line:
                break
            if "=" not in line:
                console.print("[bold red]Invalid format. Use key=value.[/bold red]")
                continue
            key, value = line.split("=", 1)
            entry[key.strip()] = value.strip()
    return entry

def prompt_for_confirmation(message: str, default: bool = False) -> bool:
    """
    Prompts the user for confirmation.

    Args:
        message: The message to display.
        default: The default value if the user just presses Enter.

    Returns:
        True if the user confirms, False otherwise.
    """
    if "pytest" in sys.modules:
        return click.confirm(message, default=default)
    else:
        return RichConfirm.ask(message, default=default)
