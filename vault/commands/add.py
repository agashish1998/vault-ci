"""The add command."""

import click
from rich.console import Console

from vault.services.vault_service import VaultService
from vault.storage import Storage
from vault.prompts import prompt_master_password, prompt_for_entry_data
from vault.exceptions import VaultNotFoundError, WrongPasswordError, EntryAlreadyExistsError

console = Console()

@click.command()
@click.argument("entry_name")
def add(entry_name):
    """Adds a new entry to the vault."""
    try:
        service = VaultService(Storage())
        password = prompt_master_password()
        entry_data = prompt_for_entry_data()
        if not entry_data:
            console.print("[yellow]No data entered. Aborting.[/yellow]")
            return
        service.add_entry(password, entry_name, entry_data)
        console.print(f"[bold green]Entry '{entry_name}' added successfully.[/bold green]")
    except (VaultNotFoundError, WrongPasswordError, EntryAlreadyExistsError) as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
