"""Tests for the CLI commands."""

import pytest
from click.testing import CliRunner
from unittest.mock import patch, Mock
import click

from vault.cli import cli
from vault.exceptions import *



@pytest.fixture
def runner():
    """Returns a CliRunner instance."""
    return CliRunner()

def test_init_command(runner: CliRunner):
    """Tests the init command."""
    with patch('vault.commands.init.VaultService') as mock_service_class:
        mock_service_instance = Mock()
        mock_service_class.return_value = mock_service_instance
        
        result = runner.invoke(cli, ['init'], input='test_password\ntest_password\n')
        
        assert result.exit_code == 0
        assert "Vault initialized successfully" in result.output
        mock_service_instance.initialize_vault.assert_called_once_with('test_password')

def test_add_command(runner: CliRunner):
    """Tests the add command."""
    with patch('vault.commands.add.VaultService') as mock_service_class:
        mock_service_instance = Mock()
        mock_service_class.return_value = mock_service_instance
        
        result = runner.invoke(cli, ['add', 'test_entry'], input='test_password\nuser=test\n\n')
        
        assert result.exit_code == 0
        assert "Entry 'test_entry' added successfully" in result.output
        # The prompt for entry data is also patched, so the input is read by click.prompt
        # which reads one line at a time. The test runner provides the lines separated by \n.
        mock_service_instance.add_entry.assert_called_once_with('test_password', 'test_entry', {'user': 'test'})

def test_get_command(runner: CliRunner):
    """Tests the get command."""
    with patch('vault.commands.get.VaultService') as mock_service_class:
        mock_service_instance = Mock()
        mock_service_instance.get_entry.return_value = {"user": "test"}
        mock_service_class.return_value = mock_service_instance
        
        result = runner.invoke(cli, ['get', 'test_entry'], input='test_password\n')
        
        assert result.exit_code == 0
        assert '"user": "test"' in result.output
        mock_service_instance.get_entry.assert_called_once_with('test_password', 'test_entry')

def test_list_command(runner: CliRunner):
    """Tests the list command."""
    with patch('vault.commands.list.VaultService') as mock_service_class:
        mock_service_instance = Mock()
        mock_service_instance.list_entries.return_value = ["entry1", "entry2"]
        mock_service_class.return_value = mock_service_instance
        
        result = runner.invoke(cli, ['list'], input='test_password\n')
        
        assert result.exit_code == 0
        assert "entry1" in result.output
        assert "entry2" in result.output
        mock_service_instance.list_entries.assert_called_once_with('test_password')

@patch('vault.commands.copy.clear_clipboard_after', Mock())
def test_copy_command(runner: CliRunner):
    """Tests the copy command."""
    with patch('vault.commands.copy.VaultService') as mock_service_class:
        mock_service_instance = Mock()
        mock_service_instance.get_entry.return_value = {"password": "supersecret"}
        mock_service_class.return_value = mock_service_instance
        
        with patch('vault.commands.copy.copy_to_clipboard') as mock_copy:
            result = runner.invoke(cli, ['copy', 'test_entry', 'password'], input='test_password\n')
            
            assert result.exit_code == 0
            assert "Copied 'password' from 'test_entry' to clipboard." in result.output
            mock_copy.assert_called_once_with('supersecret')

def test_edit_command(runner: CliRunner):
    """Tests the edit command."""
    with patch('vault.commands.edit.VaultService') as mock_service_class, \
         patch('click.edit') as mock_edit:
        
        mock_service_instance = Mock()
        mock_service_instance.get_entry.return_value = {"user": "old_user"}
        mock_service_class.return_value = mock_service_instance
        
        mock_edit.return_value = '{"user": "new_user"}'
        
        result = runner.invoke(cli, ['edit', 'test_entry'], input='test_password\n')
        
        assert result.exit_code == 0
        assert "Entry 'test_entry' updated successfully." in result.output
        mock_service_instance.update_entry.assert_called_once_with('test_password', 'test_entry', {'user': 'new_user'})