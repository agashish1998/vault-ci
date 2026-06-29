"""Configuration for the Vault application."""

from pathlib import Path

# The directory where the vault is stored.
VAULT_DIR = Path.home() / ".vault"

# The path to the encrypted vault file.
VAULT_PATH = VAULT_DIR / "vault.enc"