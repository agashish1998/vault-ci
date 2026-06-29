"""Tests for the VaultService."""

import pytest
from unittest.mock import Mock

from vault.services.vault_service import VaultService
from vault.storage import Storage
from vault.models import Vault, Entry
from vault.exceptions import EntryAlreadyExistsError, EntryNotFoundError


@pytest.fixture
def mock_storage():
    """Returns a mock Storage instance."""
    return Mock(spec=Storage)


@pytest.fixture
def vault_service(mock_storage: Mock):
    """Returns a VaultService instance with a mock storage."""
    return VaultService(mock_storage)


def test_add_entry(vault_service: VaultService, mock_storage: Mock):
    """Tests that an entry can be added."""
    password = "test_password"
    entry_name = "test_entry"
    entry_data: Entry = {"key": "value"}
    
    # Setup mock to return an empty vault
    mock_storage.load_vault.return_value = Vault(version=1, entries={})
    
    vault_service.add_entry(password, entry_name, entry_data)
    
    # Verify that load_vault was called
    mock_storage.load_vault.assert_called_once_with(password)
    
    # Verify that save_vault was called with the correct data
    saved_vault: Vault = mock_storage.save_vault.call_args[0][1]
    assert saved_vault.entries[entry_name] == entry_data


def test_add_existing_entry_raises_error(vault_service: VaultService, mock_storage: Mock):
    """Tests that adding an existing entry raises an error."""
    password = "test_password"
    entry_name = "test_entry"
    entry_data: Entry = {"key": "value"}
    
    # Setup mock to return a vault with the entry already present
    mock_storage.load_vault.return_value = Vault(version=1, entries={entry_name: {}})
    
    with pytest.raises(EntryAlreadyExistsError):
        vault_service.add_entry(password, entry_name, entry_data)


def test_get_entry(vault_service: VaultService, mock_storage: Mock):
    """Tests that an entry can be retrieved."""
    password = "test_password"
    entry_name = "test_entry"
    entry_data: Entry = {"key": "value"}
    
    # Setup mock to return a vault with the entry
    mock_storage.load_vault.return_value = Vault(version=1, entries={entry_name: entry_data})
    
    retrieved_entry = vault_service.get_entry(password, entry_name)
    
    assert retrieved_entry == entry_data


def test_get_nonexistent_entry_raises_error(vault_service: VaultService, mock_storage: Mock):
    """Tests that getting a nonexistent entry raises an error."""
    password = "test_password"
    entry_name = "test_entry"
    
    # Setup mock to return an empty vault
    mock_storage.load_vault.return_value = Vault(version=1, entries={})
    
    with pytest.raises(EntryNotFoundError):
        vault_service.get_entry(password, entry_name)

# Add more tests for other service methods (list, update, delete, search, etc.)
