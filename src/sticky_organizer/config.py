"""
Per-user persistent settings, stored as JSON in the app's home folder.

Currently holds custom categorization categories so they survive restarts.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List

logger = logging.getLogger(__name__)

APP_DIR = Path.home() / '.sticky_note_organizer'
SETTINGS_FILE = APP_DIR / 'settings.json'


def load_settings() -> dict:
    """Load settings; returns an empty structure if none exist yet."""
    try:
        with open(SETTINGS_FILE, encoding='utf-8') as fh:
            data = json.load(fh)
            if isinstance(data, dict):
                return data
    except FileNotFoundError:
        pass
    except (json.JSONDecodeError, OSError) as e:
        logger.warning("Could not read settings (%s); using defaults", e)
    return {}


def save_settings(settings: dict):
    APP_DIR.mkdir(parents=True, exist_ok=True)
    with open(SETTINGS_FILE, 'w', encoding='utf-8') as fh:
        json.dump(settings, fh, indent=2, ensure_ascii=False)


def load_custom_categories() -> Dict[str, List[str]]:
    cats = load_settings().get('custom_categories', {})
    return {str(name): [str(k) for k in kws]
            for name, kws in cats.items() if isinstance(kws, list)}


def save_custom_categories(categories: Dict[str, List[str]]):
    settings = load_settings()
    settings['custom_categories'] = categories
    save_settings(settings)
