"""The list command."""

import click
from rich.console import Console
from rich.table import Table

from vault.services.vault_service import VaultService
from vault.storage import Storage
from vault.prompts import prompt_master_password
from vault.exceptions import VaultNotFoundError, WrongPasswordError

console = Console()

@click.command("list")
def list_entries():
    """Lists all entries in the vault."""
    try:
        service = VaultService(Storage())
        password = prompt_master_password()
        entries = service.list_entries(password)
        
        if not entries:
            console.print("[yellow]No entries found in the vault.[/yellow]")
            return

        table = Table(title="Vault Entries")
        table.add_column("Entry Name", style="cyan", no_wrap=True)
        
        for entry in entries:
            table.add_row(entry)
            
        console.print(table)
    except (VaultNotFoundError, WrongPasswordError) as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
