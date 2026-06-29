"""The get command."""

import click
from rich.console import Console

from vault.services.vault_service import VaultService
from vault.storage import Storage
from vault.prompts import prompt_master_password
from vault.utils import pretty_print_json
from vault.exceptions import VaultNotFoundError, WrongPasswordError, EntryNotFoundError

console = Console()

@click.command()
@click.argument("entry_name")
def get(entry_name):
    """Retrieves an entry from the vault."""
    try:
        service = VaultService(Storage())
        password = prompt_master_password()
        entry = service.get_entry(password, entry_name)
        pretty_print_json(entry)
    except (VaultNotFoundError, WrongPasswordError, EntryNotFoundError) as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
