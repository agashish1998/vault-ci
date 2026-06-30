# Vault CLI

**Vault CLI** is a simple, secure, command-line password vault for personal use. It stores all your secret information locally on your machine in an encrypted file.

## Features

-   **Local First**: All data is stored locally. Nothing is ever uploaded to the cloud.
-   **End-to-End Encryption**: Your vault is encrypted with AES-GCM using a key derived from your master password.
-   **Tamper-Proof**: The use of an authenticated encryption cipher (AES-GCM) ensures that any tampering with the vault file is detected.
-   **Polished CLI**: A user-friendly command-line interface built with Click and Rich.
-   **Clean Architecture**: A modular and maintainable codebase that is easy to extend.

## Installation

```bash
# Clone the repository
git clone https://github.com/your-username/vault-cli.git
cd vault-cli

# Install in editable mode
pip install -e .
```

## Usage

### Initialize the vault

Before you can use the vault, you need to initialize it. This will create the encrypted vault file and prompt you for a master password.

```bash
vault init
```

### Add an entry

To add a new entry to the vault, use the `add` command. You will be prompted for your master password and then for the key-value pairs for the entry.

```bash
vault add <entry_name>
```

Example:

```bash
vault add github
Master Password: ****
username = myuser
password = mysecretpassword
<blank line to finish>
```

### Get an entry

To retrieve an entry, use the `get` command.

```bash
vault get <entry_name>
```

### List all entries

To see a list of all the entries in your vault, use the `list` command.

```bash
vault list
```

### Edit an entry

To edit an entry, use the `edit` command. This will open the entry in your default text editor.

```bash
vault edit <entry_name>
```

### Delete an entry

To delete an entry, use the `delete` command. You will be asked for confirmation.

```bash
vault delete <entry_name>
```

### Search for entries

To search for entries by name, use the `search` command.

```bash
vault search <query>
```

### Copy a field to the clipboard

To copy a specific field from an entry to your clipboard, use the `copy` command. The clipboard will be automatically cleared after 30 seconds.

```bash
vault copy <entry_name> <field_name>
```

Example:

```bash
vault copy github password
```

### Generate a random password

To generate a secure, random password, use the `generate` command. The generated password is automatically copied to the clipboard.

```bash
vault generate
```

You can customize the length and character type:

```bash
# Generate a 30-character password
vault generate --length 30

# Generate a password with only letters and numbers
vault generate --type alphanumeric
```

### Change master password

To change your master password, use the `change-password` command.

```bash
vault change-password
```

### Backup the vault

To create a timestamped backup of your vault, use the `backup` command.

```bash
vault backup
```

## Architecture

The application follows a clean architecture with a clear separation of concerns.

```
CLI (Click)
↓
Commands
↓
VaultService (Business Logic)
↓
Storage (File I/O)
↓
Crypto (Encryption)
```

-   **`vault.cli`**: The main entry point of the application, built with Click.
-   **`vault.commands`**: Each CLI command is implemented as a separate module.
-   **`vault.services.vault_service`**: The core business logic of the application.
-   **`vault.storage`**: Handles reading from and writing to the encrypted vault file.
-   **`vault.crypto`**: Implements the encryption and decryption logic.
-   **`vault.models`**: Defines the data models for the application.
-   **`vault.exceptions`**: Custom exceptions for error handling.

## Security Considerations

-   **Master Password**: Your master password is the single key to your vault. Choose a strong, unique password. The password is never stored on disk.
-   **Encryption**: The vault is encrypted using AES-256-GCM, which is a modern authenticated encryption cipher.
-   **Key Derivation**: The encryption key is derived from your master password using PBKDF2-HMAC-SHA256 with 100,000 iterations.
-   **Clipboard**: When you use the `copy` command, the clipboard is automatically cleared after 30 seconds to minimize the risk of accidental exposure.

## Backup Strategy

It is highly recommended to back up your vault regularly. You can use the `backup` command to create a timestamped, encrypted backup of your vault.

```bash
vault backup
```

This will create a file like `vault-YYYY-MM-DD-HHMMSS.enc.bak` in your vault directory (`~/.vault/`). Store this backup in a safe place, such as an external hard drive or a secure cloud storage service.
