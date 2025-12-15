#!/usr/bin/env bash
# Sticky Note Organizer - GUI Launcher for Linux/Mac
# Run this script to launch the GUI

echo "========================================"
echo " Sticky Note Organizer - GUI Launcher"
echo "========================================"
echo

# Try to launch using installed command first
if command -v sticky-organizer-gui &> /dev/null; then
    echo "Launching GUI via installed command..."
    sticky-organizer-gui
elif command -v python3 &> /dev/null; then
    echo "Launching GUI via Python module..."
    python3 -m sticky_organizer.gui_launcher
elif command -v python &> /dev/null; then
    echo "Launching GUI via Python module..."
    python -m sticky_organizer.gui_launcher
else
    echo "ERROR: Python not found."
    echo "Please install Python 3.7 or later."
    exit 1
fi
