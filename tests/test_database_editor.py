"""
Tests for database extraction and editor write operations against a
synthetic plum.sqlite-style database using the real schema and real
.NET-tick timestamps.
"""

import sqlite3
from datetime import datetime

import pytest

from sticky_organizer.database import StickyNotesDatabase
from sticky_organizer.editor import NoteEditor
from sticky_organizer.timestamps import (
    datetime_to_ticks,
    format_timestamp,
    now_ticks,
    raw_to_datetime,
)

# Real schema from Microsoft Sticky Notes plum.sqlite
NOTE_SCHEMA = """
CREATE TABLE "Note" (
    "Text" varchar,
    "WindowPosition" varchar,
    "IsOpen" integer,
    "IsAlwaysOnTop" integer,
    "CreationNoteIdAnchor" varchar,
    "Theme" varchar,
    "IsFutureNote" integer,
    "RemoteId" varchar,
    "ChangeKey" varchar,
    "LastServerVersion" varchar,
    "RemoteSchemaVersion" integer,
    "IsRemoteDataInvalid" integer,
    "PendingInsightsScan" integer,
    "Type" varchar,
    "Id" varchar primary key not null,
    "ParentId" varchar,
    "CreatedAt" bigint,
    "DeletedAt" bigint,
    "UpdatedAt" bigint
)
"""


@pytest.fixture
def plum_db(tmp_path):
    """Create a synthetic plum.sqlite with two notes."""
    db_path = tmp_path / "plum.sqlite"
    con = sqlite3.connect(db_path)
    con.execute(NOTE_SCHEMA)
    t1 = datetime_to_ticks(datetime(2024, 11, 10, 12, 30, 0))
    t2 = datetime_to_ticks(datetime(2021, 11, 11, 8, 0, 0))
    con.execute(
        "INSERT INTO Note (Id, Text, Theme, Type, CreatedAt, UpdatedAt) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        ("note-1", "\\id=abc-123 Buy milk and bread", "Yellow", "Note", t1, t1))
    con.execute(
        "INSERT INTO Note (Id, Text, Theme, Type, CreatedAt, UpdatedAt) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        ("note-2", "Call the bank about the loan", "Green", "Note", t2, t2))
    con.commit()
    con.close()
    return str(db_path)


class TestTimestamps:
    def test_dotnet_ticks_roundtrip(self):
        dt = datetime(2024, 11, 10, 12, 30, 0)
        assert raw_to_datetime(datetime_to_ticks(dt)) == dt

    def test_real_dotnet_tick_value(self):
        # Value observed in a real plum.sqlite (Nov 2024)
        dt = raw_to_datetime(638668579690000000)
        assert dt is not None and dt.year == 2024

    def test_filetime_value(self):
        # FILETIME for ~2021 (1.32e17 ticks since 1601)
        dt = raw_to_datetime(132800000000000000)
        assert dt is not None and 2020 <= dt.year <= 2022

    def test_unix_seconds_and_millis(self):
        assert raw_to_datetime(1731261169).year == 2024
        assert raw_to_datetime(1731261169000).year == 2024

    def test_invalid_values(self):
        assert raw_to_datetime(None) is None
        assert raw_to_datetime(0) is None
        assert raw_to_datetime("garbage") is None

    def test_format_timestamp_default(self):
        assert format_timestamp(None) == 'Unknown'
        assert format_timestamp(None, default='x') == 'x'

    def test_now_ticks_is_dotnet_scale(self):
        assert now_ticks() > 5 * 10**17


class TestExtraction:
    def test_extract_notes_dates_are_formatted(self, plum_db):
        db = StickyNotesDatabase()
        assert db.connect(plum_db)
        notes = db.extract_notes()
        db.close()

        assert len(notes) == 2
        by_id = {n['id']: n for n in notes}
        assert by_id['note-1']['created_date'] == '2024-11-10 12:30:00'
        assert by_id['note-2']['created_date'] == '2021-11-11 08:00:00'
        # \id= marker stripped from content
        assert by_id['note-1']['content'] == 'Buy milk and bread'

    def test_soft_deleted_notes_excluded(self, plum_db):
        with NoteEditor(plum_db, auto_backup=False) as editor:
            assert editor.delete_note('note-2')

        db = StickyNotesDatabase()
        db.connect(plum_db)
        notes = db.extract_notes()
        db.close()
        assert [n['id'] for n in notes] == ['note-1']


class TestEditor:
    def _fetch(self, db_path, note_id, columns="Text, CreatedAt, UpdatedAt, DeletedAt"):
        con = sqlite3.connect(db_path)
        row = con.execute(
            f"SELECT {columns} FROM Note WHERE Id = ?", (note_id,)).fetchone()
        con.close()
        return row

    def test_update_writes_integer_ticks(self, plum_db):
        with NoteEditor(plum_db, auto_backup=False) as editor:
            assert editor.update_note('note-2', 'New content')

        text, created, updated, deleted = self._fetch(plum_db, 'note-2')
        assert text == 'New content'
        assert isinstance(updated, int) and updated > 5 * 10**17
        # And the app-facing extraction can still parse it
        assert raw_to_datetime(updated).year >= 2026

    def test_update_preserves_id_marker(self, plum_db):
        with NoteEditor(plum_db, auto_backup=False) as editor:
            assert editor.update_note('note-1', 'Buy oat milk')

        text, *_ = self._fetch(plum_db, 'note-1')
        assert text.startswith('\\id=abc-123 ')
        assert text.endswith('Buy oat milk')

    def test_update_missing_note_returns_false(self, plum_db):
        with NoteEditor(plum_db, auto_backup=False) as editor:
            assert not editor.update_note('nope', 'x')

    def test_soft_delete_sets_integer_deletedat(self, plum_db):
        with NoteEditor(plum_db, auto_backup=False) as editor:
            assert editor.delete_note('note-1')

        *_, deleted = self._fetch(plum_db, 'note-1')
        assert isinstance(deleted, int) and deleted > 5 * 10**17

    def test_permanent_delete_removes_row(self, plum_db):
        with NoteEditor(plum_db, auto_backup=False) as editor:
            assert editor.delete_note('note-1', permanent=True)
        assert self._fetch(plum_db, 'note-1') is None

    def test_merge_soft_deletes_others(self, plum_db):
        with NoteEditor(plum_db, auto_backup=False) as editor:
            merged_id = editor.merge_notes(['note-1', 'note-2'])

        # Oldest note (note-2) survives with merged content
        assert merged_id == 'note-2'
        text, *_ = self._fetch(plum_db, 'note-2')
        assert 'Call the bank' in text and 'Buy milk' in text
        # The other note is soft-deleted, not gone
        row = self._fetch(plum_db, 'note-1')
        assert row is not None and isinstance(row[3], int)

    def test_merge_requires_two_notes(self, plum_db):
        with NoteEditor(plum_db, auto_backup=False) as editor:
            with pytest.raises(ValueError):
                editor.merge_notes(['note-1'])

    def test_duplicate_copies_full_row(self, plum_db):
        with NoteEditor(plum_db, auto_backup=False) as editor:
            new_id = editor.duplicate_note('note-1')

        assert new_id
        row = self._fetch(plum_db, new_id, "Text, Theme, CreatedAt, RemoteId")
        text, theme, created, remote_id = row
        assert text == "\\id=abc-123 Buy milk and bread"
        assert theme == 'Yellow'
        assert isinstance(created, int) and created > 5 * 10**17
        assert remote_id is None  # sync fields cleared

    def test_duplicate_missing_note_returns_none(self, plum_db):
        with NoteEditor(plum_db, auto_backup=False) as editor:
            assert editor.duplicate_note('nope') is None

    def test_search_and_replace(self, plum_db):
        with NoteEditor(plum_db, auto_backup=False) as editor:
            count = editor.search_and_replace('BANK', 'credit union')
        assert count == 1
        text, *_ = self._fetch(plum_db, 'note-2')
        assert 'credit union' in text

    def test_auto_backup_created_before_write(self, plum_db, tmp_path):
        backup_dir = tmp_path / "backups"
        with NoteEditor(plum_db, auto_backup=True,
                        backup_dir=str(backup_dir)) as editor:
            editor.update_note('note-1', 'changed')

        backups = list(backup_dir.glob('*.zip'))
        assert len(backups) == 1
