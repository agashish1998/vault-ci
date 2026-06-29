import click

from vault.services.vault_service import VaultService


@click.command()
def init():

    service = VaultService()

    service.initialize()

    click.echo("Vault initialized successfully.")
