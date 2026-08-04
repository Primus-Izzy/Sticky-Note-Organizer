"""
Create Desktop and Start Menu shortcuts so the GUI opens with one click.

Run after installing:  sticky-organizer-shortcuts
"""

import subprocess
import sys
from pathlib import Path


def _pythonw() -> str:
    """Prefer pythonw.exe so no console window flashes up."""
    candidate = Path(sys.executable).with_name('pythonw.exe')
    return str(candidate if candidate.exists() else sys.executable)


def _icon() -> str:
    return str(Path(__file__).parent / 'assets' / 'icon.ico')


def _make_shortcut_ps(lnk_expr: str) -> str:
    """PowerShell snippet that writes one .lnk at the given path expression."""
    return (
        f"$lnk = {lnk_expr};"
        "$s = (New-Object -ComObject WScript.Shell).CreateShortcut($lnk);"
        f"$s.TargetPath = '{_pythonw()}';"
        "$s.Arguments = '-m sticky_organizer.gui_launcher';"
        f"$s.IconLocation = '{_icon()}';"
        "$s.Description = 'Organize and back up your Microsoft Sticky Notes';"
        "$s.Save();"
        "Write-Output $lnk"
    )


def create_shortcuts() -> list:
    """Create Desktop and Start Menu shortcuts. Returns created paths."""
    if sys.platform != 'win32':
        raise RuntimeError("Shortcuts are only supported on Windows")

    name = 'Sticky Note Organizer.lnk'
    targets = [
        f"Join-Path ([Environment]::GetFolderPath('Desktop')) '{name}'",
        f"Join-Path ([Environment]::GetFolderPath('StartMenu')) 'Programs\\{name}'",
    ]

    created = []
    for lnk_expr in targets:
        result = subprocess.run(
            ['powershell', '-NoProfile', '-NonInteractive', '-Command',
             _make_shortcut_ps(lnk_expr)],
            capture_output=True, text=True, timeout=60)
        if result.returncode == 0 and result.stdout.strip():
            created.append(result.stdout.strip())
        else:
            print(f"Warning: could not create shortcut: {result.stderr.strip()}")
    return created


def main():
    """Entry point for sticky-organizer-shortcuts"""
    try:
        created = create_shortcuts()
    except RuntimeError as e:
        print(str(e))
        sys.exit(1)

    if created:
        print("Shortcuts created - you can now open Sticky Note Organizer "
              "from your Desktop or Start Menu:")
        for path in created:
            print(f"  {path}")
    else:
        print("No shortcuts could be created.")
        sys.exit(1)


if __name__ == '__main__':
    main()
