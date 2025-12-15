@echo off
REM Sticky Note Organizer - GUI Launcher for Windows
REM Double-click this file to launch the GUI

echo ========================================
echo  Sticky Note Organizer - GUI Launcher
echo ========================================
echo.

REM Try to launch using installed command first
where sticky-organizer-gui >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Launching GUI via installed command...
    sticky-organizer-gui
    goto :end
)

REM Try using python module
echo Launching GUI via Python module...
python -m sticky_organizer.gui_launcher
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Failed to launch GUI.
    echo Please ensure the package is installed:
    echo   pip install -e .
    echo.
    pause
)

:end
