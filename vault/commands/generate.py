"""The generate command."""

import click
from rich.console import Console

from vault.utils import generate_password
from vault.clipboard import copy_to_clipboard, clear_clipboard_after

console = Console()
CLEAR_CLIPBOARD_DELAY = 30 # seconds

@click.command()
@click.option("--length", "-l", default=15, help="Length of the password.")
@click.option(
    "--type",
    "-t",
    "char_type",
    type=click.Choice(['numbers', 'alphabets', 'alphanumeric', 'alphanumeric_symbols'], case_sensitive=False),
    default='alphanumeric_symbols',
    help="Character type for the password."
)
def generate(length, char_type):
    """Generates a random password and copies it to the clipboard."""
    password = generate_password(length, char_type)
    copy_to_clipboard(password)
    console.print("[bold green]Password generated and copied to clipboard.[/bold green]")
    console.print(f"Clipboard will be cleared in {CLEAR_CLIPBOARD_DELAY} seconds.")
    clear_clipboard_after(CLEAR_CLIPBOARD_DELAY)
