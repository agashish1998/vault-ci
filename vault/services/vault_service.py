"""Core business logic for the vault."""

from typing import List, Dict
from pathlib import Path
import datetime

from vault.storage import Storage
from vault.models import Entry
from vault.exceptions import EntryNotFoundError, EntryAlreadyExistsError


class VaultService:
    """
    Orchestrates vault operations.
    """

    def __init__(self, storage: Storage):
        self._storage = storage

    def initialize_vault(self, password: str):
        """Initializes a new vault."""
        self._storage.initialize_vault(password)

    def add_entry(self, password: str, entry_name: str, entry: Entry):
        """
        Adds a new entry to the vault.

        Args:
            password: The master password.
            entry_name: The name of the new entry.
            entry: The entry data.
        """
        vault = self._storage.load_vault(password)
        if entry_name in vault.entries:
            raise EntryAlreadyExistsError(f"Entry '{entry_name}' already exists.")
        vault.entries[entry_name] = entry
        self._storage.save_vault(password, vault)

    def get_entry(self, password: str, entry_name: str) -> Entry:
        """
        Retrieves an entry from the vault.

        Args:
            password: The master password.
            entry_name: The name of the entry to retrieve.

        Returns:
            The entry data.
        """
        vault = self._storage.load_vault(password)
        if entry_name not in vault.entries:
            raise EntryNotFoundError(f"Entry '{entry_name}' not found.")
        return vault.entries[entry_name]

    def list_entries(self, password: str) -> List[str]:
        """
        Lists all entry names in the vault, sorted alphabetically.

        Args:
            password: The master password.

        Returns:
            A sorted list of entry names.
        """
        vault = self._storage.load_vault(password)
        return sorted(vault.entries.keys())

    def update_entry(self, password: str, entry_name: str, new_entry: Entry):
        """
        Updates an existing entry.

        Args:
            password: The master password.
            entry_name: The name of the entry to update.
            new_entry: The new entry data.
        """
        vault = self._storage.load_vault(password)
        if entry_name not in vault.entries:
            raise EntryNotFoundError(f"Entry '{entry_name}' not found.")
        vault.entries[entry_name] = new_entry
        self._storage.save_vault(password, vault)

    def delete_entry(self, password: str, entry_name: str):
        """
        Deletes an entry from the vault.

        Args:
            password: The master password.
            entry_name: The name of the entry to delete.
        """
        vault = self._storage.load_vault(password)
        if entry_name not in vault.entries:
            raise EntryNotFoundError(f"Entry '{entry_name}' not found.")
        del vault.entries[entry_name]
        self._storage.save_vault(password, vault)

    def search_entries(self, password: str, query: str) -> Dict[str, Entry]:
        """
        Searches for entries matching a query.

        Args:
            password: The master password.
            query: The string to search for in entry names.

        Returns:
            A dictionary of matching entries.
        """
        vault = self._storage.load_vault(password)
        results = {name: entry for name, entry in vault.entries.items() if query.lower() in name.lower()}
        return results

    def change_password(self, old_password: str, new_password: str):
        """
        Changes the master password.

        Args:
            old_password: The current master password.
            new_password: The new master password.
        """
        vault = self._storage.load_vault(old_password)
        self._storage.save_vault(new_password, vault)

    def backup(self, password: str):
        """
        Creates a timestamped backup of the vault.
        
        Args:
            password: The master password.
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H%M%S")
        backup_path = self._storage._vault_path.with_suffix(f".{timestamp}.enc.bak")
        self._storage.backup_vault(password, backup_path)