"""Main CLI entrypoint for the Vault application."""

import click

from vault.commands.init import init
from vault.commands.add import add
from vault.commands.get import get
from vault.commands.list import list_entries
from vault.commands.edit import edit
from vault.commands.delete import delete
from vault.commands.search import search
from vault.commands.copy import copy
from vault.commands.backup import backup
from vault.commands.change_password import change_password

@click.group()
def cli():
    """A simple command-line password vault."""
    pass

cli.add_command(init)
cli.add_command(add)
cli.add_command(get)
cli.add_command(list_entries)
cli.add_command(edit)
cli.add_command(delete)
cli.add_command(search)
cli.add_command(copy)
cli.add_command(backup)
cli.add_command(change_password)

if __name__ == '__main__':
    cli()