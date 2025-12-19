# GitHub Release Instructions for v1.1.0

## 📋 Quick Summary

Create a GitHub release with the Windows standalone executable attached so users can download and run without Python.

---

## 🚀 Step-by-Step Instructions

### Step 1: Go to GitHub Releases Page

**Option A: Direct Link**
1. Open your browser and go to:
   ```
   https://github.com/Primus-Izzy/Sticky-Note-Organizer/releases/new?tag=v1.1.0
   ```

**Option B: Navigate Manually**
1. Go to: https://github.com/Primus-Izzy/Sticky-Note-Organizer
2. Click "Releases" (on the right sidebar)
3. Click "Draft a new release"
4. In "Choose a tag", select `v1.1.0`

---

### Step 2: Fill in Release Details

**Release Title:**
```
Sticky Note Organizer v1.1.0
```

**Description:**
Copy the entire contents from `RELEASE_NOTES_v1.1.0.md` file located at:
```
C:\Users\EliteBook 1030G3\Videos\Sticky-Note-Organizer-Deploy-Ready\RELEASE_NOTES_v1.1.0.md
```

Or use this shortened version:

```markdown
# 🎉 Sticky Note Organizer v1.1.0

## Classic Sticky Notes Support + Windows Executable

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

## 📊 Supported Formats

| Format | Version | Status |
|--------|---------|--------|
| **plum.sqlite** | Windows 10/11 | ✅ Supported |
| **StickyNotes.snt** | Windows 7/8 | ✅ NEW! |
| **ThresholdNotes.snt** | Windows 10 Legacy | ✅ NEW! |

---

## 🙏 Acknowledgments

Thank you to all users who requested classic sticky notes support!

Special thanks to the community for testing and feedback.

---

**Full Changelog**: [v1.0.0...v1.1.0](https://github.com/Primus-Izzy/Sticky-Note-Organizer/compare/v1.0.0...v1.1.0)

---

<div align="center">

**⭐ Star this repo if you find it useful! ⭐**

Made with ❤️ for better note organization

</div>
```

---

### Step 3: Attach Executable Files

**Important:** Attach the Windows executable as a release asset.

1. Scroll down to the "Attach binaries" section
2. Click "Attach binaries by dropping them here or selecting them"
3. Navigate to:
   ```
   C:\Users\EliteBook 1030G3\Videos\Sticky-Note-Organizer-Deploy-Ready\dist\
   ```
4. **Upload this file:**
   - `StickyNoteOrganizer-GUI.exe` (7 MB) ⭐ **REQUIRED**

5. **Optional (NOT recommended due to large size):**
   - `StickyNoteOrganizer-CLI.exe` (98 MB) - Only if you want to provide it

**Recommended:** Upload GUI only, and direct CLI users to use `pip install`

---

### Step 4: Configure Release Options

**Settings:**
- ✅ **Set as the latest release** (check this box)
- ✅ **Create a discussion for this release** (optional, recommended)
- ⬜ **Set as a pre-release** (leave unchecked)

---

### Step 5: Publish Release

1. Review all details
2. Click **"Publish release"** (green button)
3. Wait for the release to be created

---

## ✅ Verification Steps

After publishing, verify the release:

1. **Go to releases page:**
   ```
   https://github.com/Primus-Izzy/Sticky-Note-Organizer/releases
   ```

2. **Check that you see:**
   - ✅ v1.1.0 is marked as "Latest"
   - ✅ Release notes are displayed
   - ✅ `StickyNoteOrganizer-GUI.exe` appears under "Assets"
   - ✅ Download counter is visible

3. **Test the download:**
   - Click on `StickyNoteOrganizer-GUI.exe`
   - Download should start
   - File size should be ~7 MB

---

## 📢 After Release

### Update README Badge (Optional)

Add a release badge to README.md:

```markdown
[![GitHub Release](https://img.shields.io/github/v/release/Primus-Izzy/Sticky-Note-Organizer)](https://github.com/Primus-Izzy/Sticky-Note-Organizer/releases/latest)
```

### Announce the Release

Consider announcing on:
- GitHub Discussions
- Reddit (r/Python, r/productivity)
- Twitter/X
- Product Hunt
- Your personal blog

### Sample Announcement

```
🎉 Sticky Note Organizer v1.1.0 is now live!

New features:
✅ Windows standalone .exe (no Python needed!)
✅ Classic Sticky Notes (.snt) support for Windows 7/8
✅ Available on PyPI: pip install sticky-note-organizer

Download: https://github.com/Primus-Izzy/Sticky-Note-Organizer/releases/latest

#Python #Windows #Productivity #OpenSource
```

---

## 🔧 Troubleshooting

### "Tag already exists" error
- The tag v1.1.0 has been created and pushed
- Select it from the dropdown instead of creating a new one

### Can't upload file
- Check file size (7 MB is well within GitHub's 2 GB limit)
- Try a different browser
- Ensure you're logged in with proper permissions

### Release not showing as "Latest"
- Edit the release
- Check "Set as the latest release"
- Save changes

---

## 📁 File Locations

All files needed for the release:

| File | Location | Purpose |
|------|----------|---------|
| `StickyNoteOrganizer-GUI.exe` | `dist/StickyNoteOrganizer-GUI.exe` | Main executable to upload |
| `RELEASE_NOTES_v1.1.0.md` | Root directory | Release description content |
| `WINDOWS_EXECUTABLE_GUIDE.md` | Root directory | Referenced in release notes |

---

## ✨ Release Checklist

Before publishing, verify:

- [ ] Tag is set to `v1.1.0`
- [ ] Title is "Sticky Note Organizer v1.1.0"
- [ ] Description includes executable information
- [ ] `StickyNoteOrganizer-GUI.exe` is attached (7 MB)
- [ ] "Set as latest release" is checked
- [ ] Links in description are working
- [ ] PyPI link is included (https://pypi.org/project/sticky-note-organizer/)

---

## 🎯 Expected Result

After completing these steps:

1. ✅ Users can download `StickyNoteOrganizer-GUI.exe` from GitHub
2. ✅ Non-Python users can run the app instantly
3. ✅ Python users are directed to `pip install`
4. ✅ Release is visible and professional
5. ✅ All installation methods are documented

---

**Next Step:** Follow the instructions above to create the release on GitHub!

Once published, your release will be live at:
```
https://github.com/Primus-Izzy/Sticky-Note-Organizer/releases/tag/v1.1.0
```
