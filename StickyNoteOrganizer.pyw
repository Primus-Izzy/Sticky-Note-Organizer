#!/usr/bin/env python3
"""
Sticky Note Organizer - GUI Launcher (No Console Window)

Double-click this file to launch the GUI application.
"""

import sys
import os

try:
    from sticky_organizer.gui import StickyNoteGUI

    # Launch GUI
    app = StickyNoteGUI()
    app.mainloop()

except ImportError as e:
    # Show error in GUI if possible
    try:
        import tkinter as tk
        from tkinter import messagebox

        root = tk.Tk()
        root.withdraw()

        messagebox.showerror(
            "Import Error",
            f"Failed to import required modules:\n{e}\n\n"
            "Please install the package:\n"
            "pip install -e ."
        )
    except:
        # Fallback to console
        print(f"Error: {e}")
        print("\nPlease install the package with: pip install -e .")
        input("Press Enter to exit...")

except Exception as e:
    # Show any other errors
    try:
        import tkinter as tk
        from tkinter import messagebox

        root = tk.Tk()
        root.withdraw()

        messagebox.showerror(
            "Error",
            f"An error occurred:\n{e}\n\n"
            "Check the console for details."
        )
    except:
        print(f"Error: {e}")
        input("Press Enter to exit...")
