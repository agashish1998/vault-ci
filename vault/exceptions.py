"""Custom exceptions for the Vault application."""


class VaultError(Exception):
    """Base exception for all vault-related errors."""


class VaultExistsError(VaultError):
    """Raised when trying to initialize a vault that already exists."""


class VaultNotFoundError(VaultError):
    """Raised when the vault file is not found."""


class CorruptedVaultError(VaultError):
    """Raised when the vault file is corrupted or cannot be decrypted."""


class WrongPasswordError(CorruptedVaultError):
    """Raised when the provided password is incorrect."""


class EntryNotFoundError(VaultError):
    """Raised when an entry is not found in the vault."""


class EntryAlreadyExistsError(VaultError):
    """Raised when trying to add an entry that already exists."""


class InvalidJsonError(VaultError):
    """Raised when edited entry is not a valid JSON."""
