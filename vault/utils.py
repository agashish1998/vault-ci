"""Utility functions for the Vault application."""

import json
import random
import string
from rich.console import Console
from rich.json import JSON

console = Console()

def pretty_print_json(data: dict):
    """
    Pretty-prints a dictionary as JSON.

    Args:
        data: The dictionary to print.
    """
    console.print(JSON(json.dumps(data)))

def generate_password(length: int = 15, char_type: str = "alphanumeric_symbols") -> str:
    """
    Generates a random password.

    Args:
        length: The length of the password.
        char_type: The type of characters to use. 
                   Can be 'numbers', 'alphabets', 'alphanumeric', or 'alphanumeric_symbols'.

    Returns:
        The generated password.
    """
    if char_type == "numbers":
        chars = string.digits
    elif char_type == "alphabets":
        chars = string.ascii_letters
    elif char_type == "alphanumeric":
        chars = string.ascii_letters + string.digits
    else:  # alphanumeric_symbols
        chars = string.ascii_letters + string.digits + string.punctuation

    if char_type == "alphanumeric_symbols":
        # Ensure at least one of each character type for strong passwords
        password = [
            random.choice(string.ascii_lowercase),
            random.choice(string.ascii_uppercase),
            random.choice(string.digits),
            random.choice(string.punctuation)
        ]
        # Fill the rest of the password length with random characters
        for _ in range(length - 4):
            password.append(random.choice(chars))
        
        random.shuffle(password)
        return "".join(password)
    
    return "".join(random.choice(chars) for _ in range(length))

