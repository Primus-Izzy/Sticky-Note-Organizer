"""
Note editing, merging, and management functionality.

All write operations target the live Sticky Notes database, so this module
is deliberately conservative:

- Timestamps are written as .NET DateTime ticks (integers), matching what
  the Sticky Notes app stores — never ISO strings.
- Deletes are soft by default (DeletedAt is set), like the app itself.
- An automatic safety backup of the database is created before the first
  write operation of each session.
- Close the Microsoft Sticky Notes app before editing; it keeps the
  database open and may overwrite or lock changes.
"""

import logging
import re
import sqlite3
import uuid
from pathlib import Path
from typing import List, Dict, Any, Optional

from .timestamps import now_ticks

logger = logging.getLogger(__name__)

# Text stored by modern Sticky Notes can contain "\id=<guid>" markers that
# the app uses internally. We preserve them when rewriting note content.
_ID_MARKER_RE = re.compile(r'\\id=[\w\-_]+\s*')

# Sync-related columns that must not be copied into new rows, otherwise the
# app's cloud sync can conflict or silently drop the note.
_SYNC_COLUMNS = {'RemoteId', 'ChangeKey', 'LastServerVersion'}


class NoteEditor:
    """Edit, merge, and manage sticky notes in the database"""

    def __init__(self, db_path: str, auto_backup: bool = True,
                 backup_dir: Optional[str] = None):
        """
        Initialize note editor.

        Args:
            db_path: Path to the sticky notes database
            auto_backup: Create a safety backup before the first write
            backup_dir: Where to store safety backups
                        (default: ~/.sticky_note_organizer/auto_backups)
        """
        self.db_path = db_path
        self.connection = None
        self.auto_backup = auto_backup
        self.backup_dir = backup_dir or str(
            Path.home() / '.sticky_note_organizer' / 'auto_backups')
        self._backup_done = False

    def connect(self) -> bool:
        """Connect to the database. Returns True on success."""
        try:
            self.connection = sqlite3.connect(self.db_path, timeout=5.0)
            return True
        except sqlite3.Error as e:
            logger.error("Error connecting to database: %s", e)
            return False

    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            self.connection = None

    def _require_connection(self):
        if not self.connection:
            raise RuntimeError("Not connected to database")

    def _ensure_backup(self):
        """Create a one-time safety backup before the first write operation."""
        if self._backup_done or not self.auto_backup:
            return
        try:
            from .backup import BackupManager
            backup_mgr = BackupManager(self.backup_dir)
            backup_file = backup_mgr.auto_backup(self.db_path, keep_last_n=10)
            logger.info("Safety backup created: %s", backup_file)
        except Exception as e:
            # A failed backup should not corrupt-proof us into never editing,
            # but the user must know about it.
            logger.warning("Could not create safety backup: %s", e)
        self._backup_done = True

    @staticmethod
    def _preserve_id_markers(old_text: Optional[str], new_content: str) -> str:
        """Carry the app's internal \\id= markers over to rewritten content."""
        if not old_text:
            return new_content
        markers = _ID_MARKER_RE.findall(old_text)
        if not markers:
            return new_content
        if _ID_MARKER_RE.search(new_content):
            return new_content
        return ''.join(m if m.endswith(' ') else m + ' ' for m in markers) + new_content

    def update_note(self, note_id: str, new_content: str) -> bool:
        """
        Update the content of a note.

        Returns True if a note was updated.
        """
        self._require_connection()
        self._ensure_backup()

        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT Text FROM Note WHERE Id = ?", (note_id,))
            row = cursor.fetchone()
            if row is None:
                return False

            content = self._preserve_id_markers(row[0], new_content)
            cursor.execute(
                "UPDATE Note SET Text = ?, UpdatedAt = ? WHERE Id = ?",
                (content, now_ticks(), note_id))
            self.connection.commit()
            return cursor.rowcount > 0

        except sqlite3.Error as e:
            self.connection.rollback()
            raise sqlite3.Error(f"Failed to update note: {e}")

    def delete_note(self, note_id: str, permanent: bool = False) -> bool:
        """
        Delete a note. Soft delete (sets DeletedAt) by default, matching the
        Sticky Notes app's own behavior; pass permanent=True to remove the row.
        """
        self._require_connection()
        self._ensure_backup()

        try:
            cursor = self.connection.cursor()
            if permanent:
                cursor.execute("DELETE FROM Note WHERE Id = ?", (note_id,))
            else:
                cursor.execute(
                    "UPDATE Note SET DeletedAt = ?, UpdatedAt = ? WHERE Id = ?",
                    (now_ticks(), now_ticks(), note_id))
            self.connection.commit()
            return cursor.rowcount > 0

        except sqlite3.Error as e:
            self.connection.rollback()
            raise sqlite3.Error(f"Failed to delete note: {e}")

    def merge_notes(self, note_ids: List[str], separator: str = "\n\n---\n\n",
                    keep_first: bool = True) -> Optional[str]:
        """
        Merge multiple notes into a single note.

        The surviving note receives the combined content; the other notes are
        soft-deleted (recoverable), not removed.

        Returns the ID of the merged note, or None if no notes were found.
        """
        self._require_connection()

        if len(note_ids) < 2:
            raise ValueError("Need at least 2 notes to merge")

        self._ensure_backup()

        try:
            cursor = self.connection.cursor()
            placeholders = ','.join('?' * len(note_ids))
            cursor.execute(f"""
                SELECT Id, Text FROM Note
                WHERE Id IN ({placeholders})
                ORDER BY CreatedAt
            """, note_ids)
            notes = cursor.fetchall()

            if not notes:
                return None

            merged_content = separator.join(n[1] for n in notes if n[1])
            ticks = now_ticks()

            if keep_first:
                merged_id = notes[0][0]
                cursor.execute(
                    "UPDATE Note SET Text = ?, UpdatedAt = ? WHERE Id = ?",
                    (merged_content, ticks, merged_id))
                others = [n[0] for n in notes[1:]]
            else:
                merged_id = self._copy_row(cursor, notes[0][0],
                                           text=merged_content)
                others = [n[0] for n in notes]

            for other_id in others:
                cursor.execute(
                    "UPDATE Note SET DeletedAt = ?, UpdatedAt = ? WHERE Id = ?",
                    (ticks, ticks, other_id))

            self.connection.commit()
            return merged_id

        except sqlite3.Error as e:
            self.connection.rollback()
            raise sqlite3.Error(f"Failed to merge notes: {e}")

    def _copy_row(self, cursor, source_id: str,
                  text: Optional[str] = None) -> str:
        """
        Insert a full copy of an existing note row with a new Id and fresh
        timestamps. Copies every column so NOT NULL/schema expectations of
        the real database are met; clears sync columns.
        """
        cursor.execute("SELECT * FROM Note WHERE Id = ?", (source_id,))
        row = cursor.fetchone()
        if row is None:
            raise sqlite3.Error(f"Source note not found: {source_id}")

        columns = [d[0] for d in cursor.description]
        values = dict(zip(columns, row))

        new_id = str(uuid.uuid4())
        ticks = now_ticks()
        values['Id'] = new_id
        if text is not None and 'Text' in values:
            values['Text'] = text
        for col in ('CreatedAt', 'UpdatedAt'):
            if col in values:
                values[col] = ticks
        if 'DeletedAt' in values:
            values['DeletedAt'] = None
        for col in _SYNC_COLUMNS:
            if col in values:
                values[col] = None

        col_list = ', '.join(f'"{c}"' for c in columns)
        placeholders = ', '.join('?' * len(columns))
        cursor.execute(
            f'INSERT INTO Note ({col_list}) VALUES ({placeholders})',
            [values[c] for c in columns])
        return new_id

    def create_note(self, content: str, theme: str = 'Yellow') -> str:
        """
        Create a brand-new note in the database.

        Returns the ID of the created note.
        """
        if not content or not content.strip():
            raise ValueError("Note content cannot be empty")

        self._require_connection()
        self._ensure_backup()

        try:
            cursor = self.connection.cursor()
            new_id = str(uuid.uuid4())
            ticks = now_ticks()
            cursor.execute("""
                INSERT INTO Note (Id, Text, Theme, Type, IsOpen,
                                  IsAlwaysOnTop, IsFutureNote, CreatedAt, UpdatedAt)
                VALUES (?, ?, ?, 'Note', 0, 0, 0, ?, ?)
            """, (new_id, content, theme, ticks, ticks))
            self.connection.commit()
            return new_id

        except sqlite3.Error as e:
            self.connection.rollback()
            raise sqlite3.Error(f"Failed to create note: {e}")

    def bulk_update_category(self, note_ids: List[str], category: str) -> int:
        """
        Store a category for multiple notes in a separate metadata table
        (the Sticky Notes schema has no category column; we never alter it).

        Returns the number of notes updated.
        """
        self._require_connection()

        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS NoteMetadata (
                    NoteId TEXT PRIMARY KEY,
                    Category TEXT,
                    Tags TEXT,
                    CustomData TEXT
                )
            """)

            updated = 0
            for note_id in note_ids:
                cursor.execute("""
                    INSERT OR REPLACE INTO NoteMetadata (NoteId, Category)
                    VALUES (?, ?)
                """, (note_id, category))
                updated += cursor.rowcount

            self.connection.commit()
            return updated

        except sqlite3.Error as e:
            self.connection.rollback()
            raise sqlite3.Error(f"Failed to update categories: {e}")

    def get_note_by_id(self, note_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a note by its ID, or None if not found."""
        self._require_connection()

        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT Id, Text, Theme, CreatedAt, UpdatedAt, DeletedAt
                FROM Note
                WHERE Id = ?
            """, (note_id,))
            row = cursor.fetchone()

            if row:
                return {
                    'id': row[0],
                    'content': row[1],
                    'theme': row[2],
                    'created_date': row[3],
                    'updated_date': row[4],
                    'deleted_date': row[5]
                }
            return None

        except sqlite3.Error as e:
            raise sqlite3.Error(f"Failed to retrieve note: {e}")

    def duplicate_note(self, note_id: str) -> Optional[str]:
        """
        Create a duplicate of a note.

        Returns the ID of the new note, or None if the source was not found.
        """
        self._require_connection()
        self._ensure_backup()

        try:
            cursor = self.connection.cursor()
            new_id = self._copy_row(cursor, note_id)
            self.connection.commit()
            return new_id

        except sqlite3.Error as e:
            self.connection.rollback()
            if "Source note not found" in str(e):
                return None
            raise sqlite3.Error(f"Failed to duplicate note: {e}")

    def search_and_replace(self, search_text: str, replace_text: str,
                           case_sensitive: bool = False,
                           note_ids: Optional[List[str]] = None) -> int:
        """
        Search and replace text across notes.

        Returns the number of notes modified.
        """
        self._require_connection()
        self._ensure_backup()

        try:
            cursor = self.connection.cursor()

            if note_ids:
                placeholders = ','.join('?' * len(note_ids))
                cursor.execute(
                    f"SELECT Id, Text FROM Note WHERE Id IN ({placeholders})",
                    note_ids)
            else:
                cursor.execute("SELECT Id, Text FROM Note")

            notes = cursor.fetchall()
            modified_count = 0
            ticks = now_ticks()

            for note_id, text in notes:
                if not text:
                    continue

                if case_sensitive:
                    new_text = text.replace(search_text, replace_text)
                else:
                    pattern = re.compile(re.escape(search_text), re.IGNORECASE)
                    new_text = pattern.sub(replace_text, text)

                if new_text != text:
                    cursor.execute(
                        "UPDATE Note SET Text = ?, UpdatedAt = ? WHERE Id = ?",
                        (new_text, ticks, note_id))
                    modified_count += 1

            self.connection.commit()
            return modified_count

        except sqlite3.Error as e:
            self.connection.rollback()
            raise sqlite3.Error(f"Failed to search and replace: {e}")

    def __enter__(self):
        """Context manager entry"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
