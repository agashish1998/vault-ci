"""The change-password command."""

import click
from rich.console import Console

from vault.services.vault_service import VaultService
from vault.storage import Storage
from vault.prompts import prompt_master_password
from vault.exceptions import VaultNotFoundError, WrongPasswordError

console = Console()

@click.command("change-password")
def change_password():
    """Changes the master password."""
    try:
        service = VaultService(Storage())
        console.print("Enter your current password.")
        old_password = prompt_master_password()
        console.print("Enter your new password.")
        new_password = prompt_master_password(confirm=True)
        
        service.change_password(old_password, new_password)
        console.print("[bold green]Master password changed successfully.[/bold green]")

    except (VaultNotFoundError, WrongPasswordError) as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
