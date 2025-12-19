# PyPI Publishing Instructions

## Prerequisites

### 1. Create PyPI Account
- Go to https://pypi.org/account/register/
- Verify your email address

### 2. Create API Token
- Log in to https://pypi.org
- Go to Account Settings → API tokens
- Click "Add API token"
- Name: "sticky-note-organizer"
- Scope: "Entire account" (or specific project after first upload)
- Copy the token (starts with `pypi-`)

### 3. Configure Twine (One-time setup)

Create a `.pypirc` file in your home directory:

**Location:** `C:\Users\EliteBook 1030G3\.pypirc`

**Content:**
```ini
[pypi]
username = __token__
password = pypi-YOUR_TOKEN_HERE

[testpypi]
username = __token__
password = pypi-YOUR_TESTPYPI_TOKEN_HERE
repository = https://test.pypi.org/legacy/
```

Replace `YOUR_TOKEN_HERE` with your actual token.

---

## Publishing Steps

### Step 1: Test on TestPyPI First (Recommended)

```bash
cd "C:\Users\EliteBook 1030G3\Videos\Sticky-Note-Organizer-Deploy-Ready"

# Upload to TestPyPI
python -m twine upload --repository testpypi dist/*

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ sticky-note-organizer
```

### Step 2: Publish to Production PyPI

```bash
# Upload to PyPI
python -m twine upload dist/*

# Verify
pip install sticky-note-organizer
```

---

## Alternative: Interactive Upload (If .pypirc not configured)

```bash
python -m twine upload dist/*
```

You'll be prompted for:
- Username: `__token__`
- Password: Your PyPI API token (paste it here)

---

## After Publishing

1. **Verify on PyPI:**
   - https://pypi.org/project/sticky-note-organizer/

2. **Test Installation:**
   ```bash
   pip install sticky-note-organizer
   ```

3. **Update README Badge:**
   Add to your GitHub README.md:
   ```markdown
   ![PyPI](https://img.shields.io/pypi/v/sticky-note-organizer)
   ![Downloads](https://img.shields.io/pypi/dm/sticky-note-organizer)
   ```

---

## Package Details

**Package Name:** sticky-note-organizer
**Version:** 1.1.0
**Files Built:**
- `sticky_note_organizer-1.1.0.tar.gz` (62 KB)
- `sticky_note_organizer-1.1.0-py3-none-any.whl` (40 KB)

**Installation Command:**
```bash
pip install sticky-note-organizer
```

**Upgrade Command:**
```bash
pip install --upgrade sticky-note-organizer
```

---

## Troubleshooting

### Error: "Package already exists"
- You can't re-upload the same version
- Increment version in setup.py and rebuild

### Error: "Invalid credentials"
- Check your API token
- Make sure you're using `__token__` as username
- Token should start with `pypi-`

### Error: "Package name taken"
- The name "sticky-note-organizer" should be available
- If taken, add a prefix like "your-sticky-note-organizer"

---

## Security Note

**Never commit .pypirc to git!**

Add to .gitignore:
```
.pypirc
*.pypirc
```

---

## Quick Reference

```bash
# Check packages
python -m twine check dist/*

# Upload to TestPyPI
python -m twine upload --repository testpypi dist/*

# Upload to PyPI
python -m twine upload dist/*
```

---

Good luck with your release! 🚀
