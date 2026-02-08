"""Parsers for YAML, JSON, and TOML configuration files."""

from __future__ import annotations

import json
import tomllib
from pathlib import Path

import yaml

SUPPORTED_EXTENSIONS = {".yaml", ".yml", ".json", ".toml"}


def parse_file(path: str) -> dict:
    """Parse a configuration file and return its contents as a dictionary.

    Auto-detects the format based on file extension.

    Args:
        path: Path to the configuration file.

    Returns:
        Parsed configuration as a dictionary.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file extension is unsupported.
    """
    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {path}")

    ext = file_path.suffix.lower()
    if ext not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file format '{ext}'. "
            f"Supported formats: {', '.join(sorted(SUPPORTED_EXTENSIONS))}"
        )

    text = file_path.read_text(encoding="utf-8")

    if ext in (".yaml", ".yml"):
        result = yaml.safe_load(text)
    elif ext == ".json":
        result = json.loads(text)
    elif ext == ".toml":
        result = tomllib.loads(text)

    if result is None:
        return {}
    if not isinstance(result, dict):
        raise ValueError(
            f"Expected a mapping at the top level of {path}, got {type(result).__name__}"
        )

    return result
