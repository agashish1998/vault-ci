"""The init command."""

import click
from rich.console import Console

from vault.services.vault_service import VaultService
from vault.storage import Storage
from vault.prompts import prompt_master_password
from vault.exceptions import VaultExistsError

console = Console()

@click.command()
def init():
    """Initializes a new vault."""
    try:
        service = VaultService(Storage())
        password = prompt_master_password(confirm=True)
        service.initialize_vault(password)
        console.print("[bold green]Vault initialized successfully.[/bold green]")
    except VaultExistsError as e:
        console.print(f"[bold red]Error: {e}[/bold red]")