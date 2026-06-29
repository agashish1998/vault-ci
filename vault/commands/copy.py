"""The copy command."""

import click
from rich.console import Console

from vault.services.vault_service import VaultService
from vault.storage import Storage
from vault.prompts import prompt_master_password
from vault.clipboard import copy_to_clipboard, clear_clipboard_after
from vault.exceptions import VaultNotFoundError, WrongPasswordError, EntryNotFoundError

console = Console()
CLEAR_CLIPBOARD_DELAY = 30 # seconds

@click.command()
@click.argument("entry_name")
@click.argument("field")
def copy(entry_name, field):
    """Copies a field from an entry to the clipboard."""
    try:
        service = VaultService(Storage())
        password = prompt_master_password()
        entry = service.get_entry(password, entry_name)
        
        if field not in entry:
            console.print(f"[bold red]Error: Field '{field}' not found in entry '{entry_name}'.[/bold red]")
            return
            
        value_to_copy = entry[field]
        copy_to_clipboard(value_to_copy)
        console.print(f"[bold green]Copied '{field}' from '{entry_name}' to clipboard.[/bold green]")
        console.print(f"Clipboard will be cleared in {CLEAR_CLIPBOARD_DELAY} seconds.")
        clear_clipboard_after(CLEAR_CLIPBOARD_DELAY)

    except (VaultNotFoundError, WrongPasswordError, EntryNotFoundError) as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
