"""Data models for the Vault application."""

from dataclasses import dataclass, asdict
from typing import Dict

Entry = Dict[str, str]

@dataclass
class Vault:
    """Represents the entire vault."""
    version: int
    entries: Dict[str, Entry]

    def to_dict(self) -> Dict:
        """Converts the vault to a dictionary."""
        return asdict(self)