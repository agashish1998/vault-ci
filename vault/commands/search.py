"""The search command."""

import click
from rich.console import Console
from rich.table import Table

from vault.services.vault_service import VaultService
from vault.storage import Storage
from vault.prompts import prompt_master_password
from vault.exceptions import VaultNotFoundError, WrongPasswordError

console = Console()

@click.command()
@click.argument("query")
def search(query):
    """Searches for entries in the vault."""
    try:
        service = VaultService(Storage())
        password = prompt_master_password()
        results = service.search_entries(password, query)
        
        if not results:
            console.print(f"[yellow]No entries found matching '{query}'.[/yellow]")
            return

        table = Table(title=f"Search Results for '{query}'")
        table.add_column("Entry Name", style="cyan", no_wrap=True)
        
        for entry_name in results:
            table.add_row(entry_name)
            
        console.print(table)
    except (VaultNotFoundError, WrongPasswordError) as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
