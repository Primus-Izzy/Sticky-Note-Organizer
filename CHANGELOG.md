# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2026-08-04

### Fixed

#### Critical: timestamp handling (data integrity)
- **Date conversion now works on real Sticky Notes databases.** Modern
  `plum.sqlite` stores timestamps as .NET DateTime ticks (epoch 0001-01-01),
  but previous versions converted them as Windows FILETIME (epoch 1601). The
  conversion overflowed and silently fell back to raw tick numbers, so dates,
  date filters, sorting, and timeline analytics never worked on modern
  databases. A new `timestamps` module autodetects .NET ticks, FILETIME, and
  Unix seconds/milliseconds.
- **Editing no longer corrupts the database.** `update_note`, `delete_note`,
  `merge_notes`, and `duplicate_note` previously wrote ISO text strings into
  the integer `CreatedAt`/`UpdatedAt`/`DeletedAt` columns. They now write
  proper tick integers that the Sticky Notes app can read.
- **Duplicating and merging notes copies the full database row** (all 19
  columns) instead of inserting a 6-column row, and clears cloud-sync fields
  (`RemoteId`, `ChangeKey`, `LastServerVersion`) so sync does not conflict.
- **Editing preserves the app's internal `\id=` markers** in note text
  instead of dropping them.
- CLI startup no longer imports pandas eagerly (multi-second delay on some
  systems); Excel support is detected without importing it.
- **Restoring a backup to a custom filename no longer deletes the file that
  has the archived name** in the target directory (the zip was extracted
  directly into the target directory; it now goes through a temp dir).

### Changed
- **Deletes are soft by default** (set `DeletedAt`, recoverable) in both CLI
  and GUI, matching the Sticky Notes app. Permanent deletion requires
  `permanent=True`.
- **Merging soft-deletes the source notes** instead of permanently removing
  them.
- **Automatic safety backup** is created in
  `~/.sticky_note_organizer/auto_backups` (last 10 kept) before the first
  write operation of each editing session.
- Modern packaging: `pyproject.toml` replaces `setup.py`; heavy dependencies
  are now optional extras (`[excel]` for pandas/openpyxl, `[gui]` for
  matplotlib/Pillow/wordcloud, `[all]` for both). Dropped the obsolete
  `pathlib2` dependency. Minimum Python is now 3.8.
- Library modules use `logging` instead of `print`.
- `--version` now reports the real package version (was hardcoded).

### Improved
- **Smarter categorization**: keywords now match whole words with light
  suffix stemming ("business" matches "businesses") instead of raw
  substrings ("do" no longer matches "download"). Phrases score double,
  and strong signals (currency amounts, URLs, code) boost their category
  instead of overriding everything. Phone numbers and emails still route
  straight to Contacts.
- **GUI usability overhaul for non-technical users**: clear "found your
  notes automatically" status, welcome guidance when no database is found,
  note list shows dates, friendly empty states and plain-language dialogs,
  exports go to Documents/Sticky Notes Exports with an "open folder"
  prompt, backups live in a fixed per-user folder, and larger readable
  fonts.
- **Backup Restore and Delete buttons now actually work** (they were
  unimplemented stubs showing "implementation in progress").
- **One-click launch**: new `sticky-organizer-shortcuts` command creates
  Desktop and Start Menu shortcuts with a proper app icon (also run
  automatically by `install.py`); the GUI window now has an icon too.
- **Import notes**: File > Import Notes... adds notes to Sticky Notes from
  .txt (use a `---` line between notes), .csv (content column), or .json
  (this tool's export format) - with preview, confirmation, and automatic
  safety backup. New `NoteEditor.create_note()` API.
- **Statistics fill in automatically** when the tab is opened (the button
  is now just a refresh).
- **Settings tab rebuilt**: browse every category and its keywords, add
  custom categories that are saved to `~/.sticky_note_organizer/settings.json`
  and re-applied on every launch (previously lost on restart), remove
  custom categories, and see immediately how many notes match.
- **Fixed: creating a backup crashed on fresh machines** (backup folder
  was created without parent directories).

### Fixed (GUI)
- Clicking a search result opened the wrong note (selection indexed into
  the unfiltered list).
- About dialog showed a stale version number.

### Added
- GitHub Actions CI (tests on Windows and Ubuntu, Python 3.9-3.13; build +
  `twine check`) and a PyPI Trusted Publishing release workflow.
- Test suite for database extraction, timestamp conversion, and all editor
  operations against a synthetic database using the real plum.sqlite schema
  (45 tests total, up from 25).

## [1.1.1] - 2024-12-19

### Added

#### Windows Standalone Executable
- **StickyNoteOrganizer-GUI.exe** - Standalone Windows executable (7 MB)
  - No Python installation required
  - Complete GUI functionality bundled
  - Built with PyInstaller 6.17.0
  - Perfect for non-technical Windows users
- **cli_launcher.py** - Proper entry point for CLI executable
- **WINDOWS_EXECUTABLE_GUIDE.md** - Comprehensive guide for standalone executables
- **GITHUB_RELEASE_INSTRUCTIONS.md** - Step-by-step release creation guide

### Changed
- Updated README.md with Windows executable installation option
- Updated installation instructions to prioritize different user types
- Enhanced documentation for distribution options

### Fixed
- Version display in CLI now correctly shows package version
- Improved package metadata and entry points

---

## [1.1.0] - 2024-12-15

### Added

#### Classic Sticky Notes Support
- **Full support for .snt file format** (Windows 7/8/early 10)
  - New `ClassicStickyNotesParser` class for parsing .snt files
  - Extracts text content from RTF-formatted classic sticky notes
  - Supports multiple encoding methods (UTF-8, UTF-16, Latin-1)
  - Automatic detection and handling of classic .snt format
- **Updated database auto-detection** to find .snt files
  - Searches standard Windows 7/8 locations
  - Supports both `StickyNotes.snt` and `ThresholdNotes.snt`
- **Seamless integration** with existing tools
  - Works with all CLI commands
  - Works with GUI interface
  - Same export formats available
  - Same categorization system applies

### Changed
- Enhanced `StickyNotesDatabase.connect()` to handle .snt files
- Enhanced `StickyNotesDatabase.extract_notes()` to parse .snt format
- Updated documentation to reflect .snt support

### Technical Details
- **Binary format parsing** for proprietary .snt structure
- **RTF content extraction** with multiple fallback methods
- **Robust error handling** for corrupted or unusual .snt files
- **Backward compatible** - existing functionality unchanged

---

## [1.0.0] - 2024-12-15

### Added

#### GUI Features
- **Full Tkinter-based GUI application** with 5 main tabs
  - Browser tab for viewing and editing notes
  - Filter tab with advanced filtering and live preview
  - Statistics tab with charts and analytics
  - Backup tab for backup/restore operations
  - Settings tab for configuration
- **Easy GUI launchers** for non-technical users
  - `StickyNoteOrganizer.pyw` - Windows launcher without console
  - `launch_gui.bat` - Batch file launcher
  - `launch_gui.py` - Python launcher script
- **Visual statistics dashboard** with matplotlib charts
  - Category distribution pie chart
  - Word frequency analysis
  - Timeline charts
- **Note management features**
  - Edit notes directly in GUI
  - Delete notes with confirmation
  - Merge multiple notes
  - Find duplicate notes

#### Core Features
- **Backup and restore functionality**
  - Create compressed ZIP backups
  - Restore from backup with safety backup
  - List and manage backups
  - Automatic backup before destructive operations
- **Advanced filtering system**
  - Filter by date range
  - Filter by categories (multiple selection)
  - Filter by content length
  - Filter by keywords
  - Filter by theme/color
  - Chainable filter API
- **Note editing capabilities**
  - Edit note content
  - Merge multiple notes with separator
  - Delete notes safely
  - Bulk categorization
- **Analytics and insights**
  - Word frequency analysis with stop words filtering
  - Category statistics
  - Timeline analysis
  - Duplicate detection using Jaccard similarity

#### CLI Commands
- `sticky-organizer backup` - Create database backup
- `sticky-organizer restore` - Restore from backup
- `sticky-organizer edit` - Edit note by ID
- `sticky-organizer merge` - Merge multiple notes
- `sticky-organizer gui` - Launch GUI application

#### Documentation
- Comprehensive README.md with GUI guide
- CONTRIBUTING.md for contributors
- Detailed CLI command reference
- API usage examples
- Troubleshooting guide

### Changed
- **Improved categorization accuracy**
  - Fixed contact detection to check before URL patterns
  - Better regex patterns for phone numbers and emails
  - Improved keyword matching
- **Enhanced Windows console support**
  - Multi-level encoding fallback system
  - Graceful degradation from colored → plain → ASCII output
  - Added flush=True to prevent buffer issues
  - Handles cp1252 encoding properly
- **Better error handling**
  - Try-except blocks for encoding errors
  - Validation for note IDs and paths
  - User-friendly error messages

### Fixed
- **Windows console encoding issues** - Fixed UnicodeEncodeError and OSError when piping output
- **Summary export parameter mismatch** - Fixed 'list' object has no attribute 'items' error
- **None content handling** - Fixed AttributeError when note content is None
- **Contact categorization** - Improved to correctly categorize notes with emails/phones
- **Unicode character handling** - Robust handling of special characters in note content

### Technical Improvements
- Added context manager support for NoteEditor
- Fluent API for filters with method chaining
- Separate exporters for different formats
- Comprehensive test suite (25 unit tests + 7 integration tests)
- 100% test pass rate

## [0.1.0] - Initial Release

### Added
- Basic CLI functionality
- Note extraction from Microsoft Sticky Notes database
- Automatic categorization into 12+ categories
- Export to CSV, JSON, Markdown formats
- Basic search functionality
- Database auto-detection
- Console colored output

---

## Types of Changes

- **Added** for new features
- **Changed** for changes in existing functionality
- **Deprecated** for soon-to-be removed features
- **Removed** for now removed features
- **Fixed** for any bug fixes
- **Security** in case of vulnerabilities
