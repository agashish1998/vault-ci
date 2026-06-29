"""Tests for the storage module."""

import pytest

from vault.storage import Storage
from vault.models import Vault
from vault.exceptions import VaultExistsError, VaultNotFoundError, WrongPasswordError


@pytest.fixture
def storage(tmp_path):
    """Returns a Storage instance with a temporary vault path."""
    vault_path = tmp_path / "vault.enc"
    return Storage(vault_path)


def test_initialize_vault(storage: Storage):
    """Tests that a vault can be initialized."""
    password = "test_password"
    storage.initialize_vault(password)
    assert storage.vault_exists()


def test_initialize_existing_vault_raises_error(storage: Storage):
    """Tests that initializing an existing vault raises an error."""
    password = "test_password"
    storage.initialize_vault(password)
    
    with pytest.raises(VaultExistsError):
        storage.initialize_vault(password)


def test_load_vault(storage: Storage):
    """Tests that a vault can be loaded."""
    password = "test_password"
    storage.initialize_vault(password)
    
    vault = storage.load_vault(password)
    assert isinstance(vault, Vault)
    assert vault.version == 1
    assert vault.entries == {}


def test_load_nonexistent_vault_raises_error(storage: Storage):
    """Tests that loading a nonexistent vault raises an error."""
    with pytest.raises(VaultNotFoundError):
        storage.load_vault("test_password")


def test_load_vault_wrong_password_raises_error(storage: Storage):
    """Tests that loading a vault with the wrong password raises an error."""
    password = "test_password"
    wrong_password = "wrong_password"
    storage.initialize_vault(password)
    
    with pytest.raises(WrongPasswordError):
        storage.load_vault(wrong_password)


def test_save_and_load_vault(storage: Storage):
    """Tests that a vault can be saved and loaded."""
    password = "test_password"
    storage.initialize_vault(password)
    
    # Create a vault with some data
    vault = Vault(version=1, entries={"test_entry": {"key": "value"}})
    storage.save_vault(password, vault)
    
    # Load the vault and check the data
    loaded_vault = storage.load_vault(password)
    assert loaded_vault.entries["test_entry"]["key"] == "value"


def test_backup_vault(storage: Storage, tmp_path):
    """Tests that a vault can be backed up."""
    password = "test_password"
    storage.initialize_vault(password)
    
    backup_path = tmp_path / "vault.bak"
    storage.backup_vault(password, backup_path)
    
    assert backup_path.exists()
