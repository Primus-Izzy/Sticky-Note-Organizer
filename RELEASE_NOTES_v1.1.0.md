# 🎉 Sticky Note Organizer v1.1.0

## Classic Sticky Notes Support

We're excited to announce v1.1.0 with full support for **Classic Sticky Notes (.snt format)** from Windows 7/8/early Windows 10!

---

## 🌟 What's New

### 🪟 Windows Standalone Executable (NEW!)

**No Python installation required!** Download and run instantly.

- **StickyNoteOrganizer-GUI.exe** (7 MB) - Double-click to launch
- Complete GUI functionality without any dependencies
- Perfect for non-technical Windows users
- See [WINDOWS_EXECUTABLE_GUIDE.md](WINDOWS_EXECUTABLE_GUIDE.md) for details

**Download:** Attached to this release below ⬇️

### Classic .snt Format Support

Now you can organize your old sticky notes from Windows 7 and 8!

- **Full .snt parsing** - Extract notes from legacy format
- **RTF content extraction** - Handles Rich Text Format properly
- **Auto-detection** - Automatically finds .snt files in standard locations
- **Multiple encoding support** - UTF-8, UTF-16, and Latin-1
- **Seamless integration** - Works with all existing CLI and GUI features

### Updated Features

- **Database auto-detection** now finds both modern (.sqlite) and classic (.snt) formats
- **Same great features** - Export, categorization, backup all work with .snt files
- **Backward compatible** - All v1.0.0 functionality preserved

---

## 📦 Installation

### Windows Standalone (No Python Required) 🪟
1. Download `StickyNoteOrganizer-GUI.exe` from the release assets below
2. Double-click to run - that's it!

### Via pip (Recommended for Python Users)
```bash
pip install sticky-note-organizer
```

**PyPI Package:** https://pypi.org/project/sticky-note-organizer/

### From Source
```bash
git clone https://github.com/Primus-Izzy/Sticky-Note-Organizer.git
cd Sticky-Note-Organizer
python install.py
```

---

## 🚀 Quick Start

### For Classic Sticky Notes Users

**GUI (Easiest):**
1. Double-click `StickyNoteOrganizer.pyw`
2. Click "Connect" and browse to your .snt file
3. Start organizing!

**CLI:**
```bash
# Auto-detect .snt file
sticky-organizer extract

# Specify .snt file
sticky-organizer extract -d "C:\path\to\StickyNotes.snt"

# Export to multiple formats
sticky-organizer extract -f csv json excel -d StickyNotes.snt
```

---

## 📊 Supported Formats

| Format | Version | Status |
|--------|---------|--------|
| **plum.sqlite** | Windows 10/11 | ✅ Supported |
| **StickyNotes.snt** | Windows 7/8 | ✅ NEW! |
| **ThresholdNotes.snt** | Windows 10 Legacy | ✅ NEW! |

---

## 🔧 Technical Details

### New Components

- **ClassicStickyNotesParser** class for binary .snt parsing
- Multi-method text extraction (UTF-8, UTF-16, Latin-1)
- RTF tag cleaning and content filtering
- Robust error handling for corrupted files

### Changes

- Enhanced `StickyNotesDatabase.connect()` to handle .snt files
- Enhanced `StickyNotesDatabase.extract_notes()` with .snt parser
- Updated auto-detection to search .snt locations
- Added test script `test_snt_support.py`

---

## 📖 Documentation

- [README.md](README.md) - Complete documentation
- [CHANGELOG.md](CHANGELOG.md) - Full version history
- [QUICK_START.md](docs/QUICK_START.md) - Getting started guide
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines

---

## 🎯 Use Cases

**Perfect for:**
- 📦 Migrating from Windows 7/8 to modern Windows
- 🔄 Backing up old sticky notes
- 📊 Analyzing years of notes across formats
- 💾 Preserving legacy data
- 🔍 Searching through old notes

---

## 🐛 Bug Fixes & Improvements

- Improved encoding handling for international characters
- Better RTF parsing for complex formatted notes
- Enhanced error messages for unsupported formats
- More robust file format detection

---

## 📈 Statistics

- **2 database formats** supported (modern + classic)
- **~4,800 lines** of code
- **25 unit tests** (100% passing)
- **12+ categories** for organization
- **5 export formats** available
- **Backward compatible** with v1.0.0

---

## 🙏 Acknowledgments

Thank you to all users who requested classic sticky notes support!

Special thanks to the community for testing and feedback.

---

## 🔜 What's Next

See our [Roadmap](README.md#-roadmap) for upcoming features:
- Cloud sync support
- Mobile app companion
- Advanced AI categorization
- Export to OneNote/Evernote

---

## 📞 Support

- **Issues**: [Report bugs](https://github.com/Primus-Izzy/Sticky-Note-Organizer/issues)
- **Discussions**: [Ask questions](https://github.com/Primus-Izzy/Sticky-Note-Organizer/discussions)
- **Documentation**: See [docs/](docs/) directory

---

## ⬆️ Upgrading from v1.0.0

Simply pull the latest code or reinstall:

```bash
cd Sticky-Note-Organizer
git pull origin main
python install.py
```

All your settings and workflows remain unchanged!

---

**Full Changelog**: [v1.0.0...v1.1.0](https://github.com/Primus-Izzy/Sticky-Note-Organizer/compare/v1.0.0...v1.1.0)

**Download**: [Source code (zip)](https://github.com/Primus-Izzy/Sticky-Note-Organizer/archive/refs/tags/v1.1.0.zip) | [Source code (tar.gz)](https://github.com/Primus-Izzy/Sticky-Note-Organizer/archive/refs/tags/v1.1.0.tar.gz)

---

<div align="center">

**⭐ Star this repo if you find it useful! ⭐**

Made with ❤️ for better note organization

</div>
