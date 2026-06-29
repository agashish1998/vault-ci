"""The backup command."""

import click
from rich.console import Console

from vault.services.vault_service import VaultService
from vault.storage import Storage
from vault.prompts import prompt_master_password
from vault.exceptions import VaultNotFoundError, WrongPasswordError

console = Console()

@click.command()
def backup():
    """Creates a timestamped backup of the vault."""
    try:
        service = VaultService(Storage())
        password = prompt_master_password()
        service.backup(password)
        console.print("[bold green]Vault backed up successfully.[/bold green]")
    except (VaultNotFoundError, WrongPasswordError) as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
