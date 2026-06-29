"""The delete command."""

import click
from rich.console import Console

from vault.services.vault_service import VaultService
from vault.storage import Storage
from vault.prompts import prompt_master_password, prompt_for_confirmation
from vault.exceptions import VaultNotFoundError, WrongPasswordError, EntryNotFoundError

console = Console()

@click.command()
@click.argument("entry_name")
def delete(entry_name):
    """Deletes an entry from the vault."""
    try:
        if not prompt_for_confirmation(f"Are you sure you want to delete '{entry_name}'?", default=False):
            console.print("[yellow]Aborting.[/yellow]")
            return

        service = VaultService(Storage())
        password = prompt_master_password()
        service.delete_entry(password, entry_name)
        console.print(f"[bold green]Entry '{entry_name}' deleted successfully.[/bold green]")

    except (VaultNotFoundError, WrongPasswordError, EntryNotFoundError) as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
