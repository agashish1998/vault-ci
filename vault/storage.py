"""Handles reading and writing the encrypted vault file."""

from pathlib import Path
import json

from vault import crypto
from vault.config import VAULT_PATH, VAULT_DIR
from vault.exceptions import VaultNotFoundError, VaultExistsError, CorruptedVaultError, WrongPasswordError
from vault.models import Vault


class Storage:
    """
    Manages the encrypted vault file on disk.
    """
    def __init__(self, vault_path: Path = VAULT_PATH):
        self._vault_path = vault_path

    def vault_exists(self) -> bool:
        """Checks if the vault file exists."""
        return self._vault_path.exists()

    def initialize_vault(self, password: str):
        """
        Creates a new, empty vault.

        Args:
            password: The master password for the new vault.

        Raises:
            VaultExistsError: If the vault file already exists.
        """
        if self.vault_exists():
            raise VaultExistsError("Vault already exists.")
        
        VAULT_DIR.mkdir(exist_ok=True)
        
        empty_vault = Vault(version=1, entries={})
        self.save_vault(password, empty_vault)


    def load_vault(self, password: str) -> Vault:
        """
        Loads and decrypts the vault from disk.

        Args:
            password: The master password.

        Returns:
            The decrypted vault data.

        Raises:
            VaultNotFoundError: If the vault file does not exist.
            WrongPasswordError: If the password is incorrect.
            CorruptedVaultError: If the vault is malformed.
        """
        if not self.vault_exists():
            raise VaultNotFoundError("Vault not found. Please run 'vault init' first.")

        try:
            encrypted_data = self._vault_path.read_bytes()
            decrypted_data = crypto.decrypt(password, encrypted_data)
            vault_dict = json.loads(decrypted_data)
            return Vault(**vault_dict)
        except WrongPasswordError:
            raise
        except Exception as e:
            raise CorruptedVaultError(f"Failed to load vault: {e}")


    def save_vault(self, password: str, vault: Vault):
        """
        Encrypts and saves the vault to disk.

        Args:
            password: The master password.
            vault: The vault data to save.
        """
        vault_data = json.dumps(vault.to_dict(), indent=4).encode('utf-8')
        encrypted_data = crypto.encrypt(password, vault_data)
        self._vault_path.write_bytes(encrypted_data)

    def backup_vault(self, password: str, backup_path: Path):
        """
        Creates a backup of the vault.

        Args:
            password: The master password.
            backup_path: The path to save the backup to.
        
        Raises:
            VaultNotFoundError: If the vault file does not exist.
        """
        if not self.vault_exists():
            raise VaultNotFoundError("Vault not found. Cannot create backup.")

        encrypted_data = self._vault_path.read_bytes()
        # We just copy the encrypted data, no need to decrypt and re-encrypt
        backup_path.write_bytes(encrypted_data)