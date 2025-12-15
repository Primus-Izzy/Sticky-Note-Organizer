#!/usr/bin/env python3
"""
Sticky Note Organizer - Simple GUI Launcher

Run this script to launch the GUI application.
Works on all platforms (Windows, Mac, Linux).
"""

import sys

def main():
    """Launch the GUI application"""
    print("=" * 50)
    print("  Sticky Note Organizer - GUI")
    print("=" * 50)
    print()

    try:
        from sticky_organizer.gui import StickyNoteGUI

        print("Starting GUI application...")
        app = StickyNoteGUI()
        app.mainloop()

    except ImportError as e:
        print(f"ERROR: Failed to import required modules.")
        print(f"Details: {e}")
        print()
        print("Please install the package first:")
        print("  pip install -e .")
        print()
        input("Press Enter to exit...")
        sys.exit(1)

    except Exception as e:
        print(f"ERROR: An unexpected error occurred.")
        print(f"Details: {e}")
        print()
        import traceback
        traceback.print_exc()
        print()
        input("Press Enter to exit...")
        sys.exit(1)


if __name__ == '__main__':
    main()
