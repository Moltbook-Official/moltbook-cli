"""Configuration management for Moltbook CLI."""

import json
import os
from pathlib import Path
from typing import Optional

CONFIG_DIR = Path.home() / ".moltbook"
CONFIG_FILE = CONFIG_DIR / "config.json"


def get_config_dir() -> Path:
    """Get or create config directory."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    return CONFIG_DIR


def load_config() -> dict:
    """Load config from file."""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            return json.load(f)
    return {}


def save_config(config: dict):
    """Save config to file."""
    get_config_dir()
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)


def get_api_key() -> Optional[str]:
    """Get API key from environment or config."""
    # Environment variable takes precedence
    env_key = os.environ.get("MOLTBOOK_API_KEY")
    if env_key:
        return env_key

    # Fall back to config file
    config = load_config()
    return config.get("api_key")


def set_api_key(api_key: str):
    """Set API key in config file."""
    config = load_config()
    config["api_key"] = api_key
    save_config(config)


def get_config_value(key: str) -> Optional[str]:
    """Get a config value."""
    config = load_config()
    return config.get(key)


def set_config_value(key: str, value: str):
    """Set a config value."""
    config = load_config()
    config[key] = value
    save_config(config)
