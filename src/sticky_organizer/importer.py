"""
Import notes from files into the Sticky Notes database.

Supported formats:
- .txt  - one note, or several separated by lines containing only "---"
- .csv  - uses the "content" column (falls back to the first column)
- .json - this tool's own export format, or a plain list of strings/objects
"""

import csv
import json
from pathlib import Path
from typing import List


def parse_import_file(path: str) -> List[str]:
    """
    Read a file and return the list of note contents it describes.

    Raises ValueError for unsupported or unreadable formats.
    """
    file_path = Path(path)
    suffix = file_path.suffix.lower()

    if suffix == '.json':
        return _parse_json(file_path)
    if suffix == '.csv':
        return _parse_csv(file_path)
    if suffix in ('.txt', '.md'):
        return _parse_text(file_path)

    raise ValueError(
        f"Unsupported file type: {suffix or 'no extension'}. "
        "Use a .txt, .csv, or .json file.")


def _clean(contents: List[str]) -> List[str]:
    return [c.strip() for c in contents if c and c.strip()]


def _parse_json(file_path: Path) -> List[str]:
    with open(file_path, encoding='utf-8') as fh:
        data = json.load(fh)

    # Our export format: {"notes": [{"content": ...}, ...]}
    if isinstance(data, dict) and 'notes' in data:
        data = data['notes']

    if not isinstance(data, list):
        raise ValueError("JSON file must contain a list of notes "
                         "or this tool's export format")

    contents = []
    for item in data:
        if isinstance(item, str):
            contents.append(item)
        elif isinstance(item, dict):
            text = item.get('content') or item.get('text') or item.get('Text')
            if text:
                contents.append(str(text))
    return _clean(contents)


def _parse_csv(file_path: Path) -> List[str]:
    with open(file_path, encoding='utf-8-sig', newline='') as fh:
        reader = csv.DictReader(fh)
        if not reader.fieldnames:
            return []
        # Find a content-like column, else use the first one
        field = next((f for f in reader.fieldnames
                      if f and f.lower() in ('content', 'text', 'note')),
                     reader.fieldnames[0])
        return _clean([row.get(field, '') for row in reader])


def _parse_text(file_path: Path) -> List[str]:
    text = file_path.read_text(encoding='utf-8-sig')
    # Lines containing only dashes split the file into separate notes
    parts = []
    current = []
    for line in text.splitlines():
        if line.strip() and set(line.strip()) == {'-'} and len(line.strip()) >= 3:
            parts.append('\n'.join(current))
            current = []
        else:
            current.append(line)
    parts.append('\n'.join(current))
    cleaned = _clean(parts)
    return cleaned if cleaned else _clean([text])
