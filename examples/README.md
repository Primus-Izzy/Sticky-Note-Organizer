# Examples

This directory contains example scripts and sample data to help you get started with Sticky Note Organizer.

## Files

### `basic_usage.py`

Comprehensive examples demonstrating common usage patterns:

- **Example 1**: Basic note extraction
- **Example 2**: Note categorization
- **Example 3**: Advanced filtering
- **Example 4**: Export to multiple formats
- **Example 5**: Create backup
- **Example 6**: Analytics and insights
- **Example 7**: Custom categories

**How to run:**
```bash
python examples/basic_usage.py
```

### `plum.sqlite`

Sample Microsoft Sticky Notes database file for testing purposes. Contains example notes across various categories.

**Note:** This is sample data. Your actual sticky notes database is located at:
```
%USERPROFILE%\AppData\Local\Packages\Microsoft.MicrosoftStickyNotes_8wekyb3d8bbwe\LocalState\plum.sqlite
```

## Usage Examples

### Example 1: Extract Notes

```python
from sticky_organizer.database import StickyNotesDatabase

db = StickyNotesDatabase()
if db.connect():
    notes = db.extract_notes()
    print(f"Extracted {len(notes)} notes")
    db.close()
```

### Example 2: Categorize Notes

```python
from sticky_organizer.categorizer import NoteCategorizer

categorizer = NoteCategorizer()
categorized = categorizer.categorize_notes(notes)

for category, category_notes in categorized.items():
    print(f"{category}: {len(category_notes)} notes")
```

### Example 3: Filter and Sort

```python
from sticky_organizer.filters import NoteFilter, NoteSorter

# Filter notes
filter_engine = NoteFilter()
filtered = (filter_engine
    .by_content_length(min_length=50)
    .by_keywords(['business', 'startup'])
    .apply(notes))

# Sort by date
sorted_notes = NoteSorter.by_date(filtered, ascending=False)
```

### Example 4: Export

```python
from sticky_organizer.exporters import ExportManager

export_manager = ExportManager('output')
results = export_manager.export(notes, ['csv', 'json', 'excel'], 'my_notes')
```

### Example 5: Create Backup

```python
from sticky_organizer.backup import BackupManager

backup_mgr = BackupManager('backups')
backup_file = backup_mgr.create_backup('path/to/plum.sqlite', compress=True)
print(f"Backup created: {backup_file}")
```

### Example 6: Analytics

```python
from sticky_organizer.analytics import AdvancedAnalytics

analytics = AdvancedAnalytics()

# Word frequency
word_freq = analytics.get_word_frequency(notes, top_n=20)

# Category stats
categorizer = NoteCategorizer()
categorized = categorizer.categorize_notes(notes)
stats = analytics.get_category_stats(categorized)
```

## Testing with Sample Data

You can test the tool with the included sample database:

```bash
# Extract notes from sample database
sticky-organizer extract -d examples/plum.sqlite -o test_output

# Search in sample database
sticky-organizer search "business" -d examples/plum.sqlite

# Create backup of sample database
sticky-organizer backup -d examples/plum.sqlite -o test_backups
```

## Creating Your Own Examples

Feel free to create your own example scripts based on these patterns. Share them with the community by submitting a pull request!

## Need Help?

- Check the main [README.md](../README.md) for full documentation
- See [QUICK_START.md](../docs/QUICK_START.md) for getting started guide
- Open an issue on GitHub for questions
