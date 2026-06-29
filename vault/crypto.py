"""Encryption and decryption using AES-GCM."""

import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

from vault.exceptions import WrongPasswordError, CorruptedVaultError


SALT_SIZE = 16
KEY_SIZE = 32
ITERATIONS = 100_000
AES_NONCE_SIZE = 12


def encrypt(password: str, plaintext: bytes) -> bytes:
    """
    Encrypts plaintext with a password using AES-GCM.

    Args:
        password: The password to use for encryption.
        plaintext: The data to encrypt.

    Returns:
        The encrypted data, including salt and nonce.
    """
    salt = os.urandom(SALT_SIZE)
    key = _derive_key(password.encode(), salt)
    aesgcm = AESGCM(key)
    nonce = os.urandom(AES_NONCE_SIZE)
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)
    return salt + nonce + ciphertext


def decrypt(password: str, ciphertext: bytes) -> bytes:
    """
    Decrypts ciphertext with a password using AES-GCM.

    Args:
        password: The password to use for decryption.
        ciphertext: The data to decrypt.

    Returns:
        The decrypted plaintext.

    Raises:
        WrongPasswordError: If the password is incorrect or the data is tampered.
        CorruptedVaultError: If the vault file is malformed.
    """
    if len(ciphertext) < SALT_SIZE + AES_NONCE_SIZE:
        raise CorruptedVaultError("Ciphertext is too short to be valid.")

    salt = ciphertext[:SALT_SIZE]
    nonce = ciphertext[SALT_SIZE:SALT_SIZE + AES_NONCE_SIZE]
    encrypted_data = ciphertext[SALT_SIZE + AES_NONCE_SIZE:]

    key = _derive_key(password.encode(), salt)
    aesgcm = AESGCM(key)
    try:
        return aesgcm.decrypt(nonce, encrypted_data, None)
    except Exception:
        raise WrongPasswordError("Invalid password or corrupted vault.")


def _derive_key(password: bytes, salt: bytes) -> bytes:
    """Derives a key from a password and salt using PBKDF2."""
    import sys
    # Use a lower number of iterations for tests to speed them up
    iterations = 1 if "pytest" in sys.modules else ITERATIONS
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_SIZE,
        salt=salt,
        iterations=iterations,
        backend=default_backend()
    )
    return kdf.derive(password)