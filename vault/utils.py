"""Utility functions for the Vault application."""

import json
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
