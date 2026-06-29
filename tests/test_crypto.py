"""Tests for the crypto module."""

import pytest

from vault.crypto import encrypt, decrypt
from vault.exceptions import WrongPasswordError


def test_encrypt_decrypt_success():
    """Tests that encrypt and decrypt work correctly."""
    password = "test_password"
    plaintext = b"test_plaintext"
    
    encrypted = encrypt(password, plaintext)
    decrypted = decrypt(password, encrypted)
    
    assert decrypted == plaintext
    assert encrypted != plaintext

def test_decrypt_wrong_password():
    """Tests that decrypt raises WrongPasswordError with the wrong password."""
    password = "test_password"
    wrong_password = "wrong_password"
    plaintext = b"test_plaintext"
    
    encrypted = encrypt(password, plaintext)
    
    with pytest.raises(WrongPasswordError):
        decrypt(wrong_password, encrypted)

def test_tampered_data():
    """Tests that decrypt raises WrongPasswordError with tampered data."""
    password = "test_password"
    plaintext = b"test_plaintext"
    
    encrypted = encrypt(password, plaintext)
    
    # Tamper with the ciphertext
    tampered_encrypted = bytearray(encrypted)
    tampered_encrypted[-1] ^= 0x01
    
    with pytest.raises(WrongPasswordError):
        decrypt(password, bytes(tampered_encrypted))
