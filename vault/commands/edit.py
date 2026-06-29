"""The edit command."""

import click
import json
from rich.console import Console

from vault.services.vault_service import VaultService
from vault.storage import Storage
from vault.prompts import prompt_master_password
from vault.exceptions import VaultNotFoundError, WrongPasswordError, EntryNotFoundError, InvalidJsonError

console = Console()

@click.command()
@click.argument("entry_name")
def edit(entry_name):
    """Edits an existing entry in the vault."""
    try:
        service = VaultService(Storage())
        password = prompt_master_password()
        
        # Get the current entry to populate the editor
        current_entry = service.get_entry(password, entry_name)
        
        # Open the user's default editor with the current entry as JSON
        edited_json = click.edit(json.dumps(current_entry, indent=4))
        
        if edited_json is None:
            console.print("[yellow]No changes made. Aborting.[/yellow]")
            return
            
        try:
            new_entry = json.loads(edited_json)
        except json.JSONDecodeError:
            raise InvalidJsonError("The edited content is not valid JSON.")
            
        service.update_entry(password, entry_name, new_entry)
        console.print(f"[bold green]Entry '{entry_name}' updated successfully.[/bold green]")

    except (VaultNotFoundError, WrongPasswordError, EntryNotFoundError, InvalidJsonError) as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
