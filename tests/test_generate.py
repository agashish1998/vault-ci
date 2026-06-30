"""Tests for the generate command and password generation utility."""

import string
import pytest
from click.testing import CliRunner
from unittest.mock import patch, Mock

from vault.cli import cli
from vault.utils import generate_password

def test_generate_password_length():
    """Tests that the generated password has the correct length."""
    assert len(generate_password(length=10)) == 10
    assert len(generate_password(length=20)) == 20

def test_generate_password_char_types():
    """Tests the character types of the generated password."""
    assert all(c in string.digits for c in generate_password(char_type='numbers'))
    assert all(c in string.ascii_letters for c in generate_password(char_type='alphabets'))
    assert all(c in string.ascii_letters + string.digits for c in generate_password(char_type='alphanumeric'))

def test_generate_password_strong():
    """Tests that the default strong password contains all required character types."""
    password = generate_password(length=15, char_type='alphanumeric_symbols')
    assert any(c in string.ascii_lowercase for c in password)
    assert any(c in string.ascii_uppercase for c in password)
    assert any(c in string.digits for c in password)
    assert any(c in string.punctuation for c in password)

@pytest.fixture
def runner():
    """Returns a CliRunner instance."""
    return CliRunner()

@patch('vault.commands.generate.clear_clipboard_after', Mock())
def test_generate_command(runner: CliRunner):
    """Tests the generate command."""
    with patch('vault.commands.generate.copy_to_clipboard') as mock_copy:
        result = runner.invoke(cli, ['generate', '--length', '20'])
        
        assert result.exit_code == 0
        assert "Password generated and copied to clipboard." in result.output
        
        # Check that the generated password has the correct length
        generated_password = mock_copy.call_args[0][0]
        assert len(generated_password) == 20
