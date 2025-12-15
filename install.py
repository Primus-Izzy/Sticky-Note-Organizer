#!/usr/bin/env python3
"""
Installation script for Sticky Note Organizer
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors"""
    print(f"📦 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed!")
        print(f"Error: {e.stderr}")
        return False


def check_python_version():
    """Check if Python version is supported"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print(f"❌ Python 3.7+ is required. You have Python {version.major}.{version.minor}")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is supported")
    return True


def install_dependencies():
    """Install required dependencies"""
    print("🔧 Installing dependencies...")
    
    # Core dependencies
    core_deps = [
        "click>=8.0.0",
        "colorama>=0.4.0",
        "pathlib2>=2.3.0",
        "python-dateutil>=2.8.0"
    ]
    
    # Optional dependencies
    optional_deps = [
        "pandas>=1.3.0",
        "openpyxl>=3.0.0",
        "tabulate>=0.8.0"
    ]
    
    # Install core dependencies
    for dep in core_deps:
        if not run_command(f"pip install {dep}", f"Installing {dep.split('>=')[0]}"):
            return False
    
    # Try to install optional dependencies
    print("\n📋 Installing optional dependencies for enhanced features...")
    for dep in optional_deps:
        run_command(f"pip install {dep}", f"Installing {dep.split('>=')[0]} (optional)")
    
    return True


def setup_development_environment():
    """Set up development environment"""
    print("\n🛠️  Setting up development environment...")
    
    # Install package in development mode
    if not run_command("pip install -e .", "Installing Sticky Note Organizer in development mode"):
        return False
    
    return True


def create_example_config():
    """Create example configuration files"""
    print("📝 Creating example files...")
    
    # Create example directory
    examples_dir = Path("examples")
    examples_dir.mkdir(exist_ok=True)
    
    # Example usage script
    example_script = examples_dir / "example_usage.py"
    with open(example_script, 'w', encoding='utf-8') as f:
        f.write('''#!/usr/bin/env python3
"""
Example usage of Sticky Note Organizer
"""

from sticky_organizer.database import StickyNotesDatabase
from sticky_organizer.categorizer import NoteCategorizer
from sticky_organizer.exporters import ExportManager

def main():
    """Example usage"""
    
    # Connect to database
    db = StickyNotesDatabase()
    if not db.connect():
        print("Could not connect to database")
        return
    
    # Extract notes
    notes = db.extract_notes()
    print(f"Found {len(notes)} notes")
    
    # Categorize notes
    categorizer = NoteCategorizer()
    categorized = categorizer.categorize_notes(notes)
    
    # Export to different formats
    export_manager = ExportManager()
    results = export_manager.export(notes, ['csv', 'json'], 'my_notes')
    
    for format_type, filepath in results.items():
        print(f"Exported {format_type}: {filepath}")
    
    db.close()

if __name__ == "__main__":
    main()
''')
    
    print(f"✅ Created example script: {example_script}")
    return True


def main():
    """Main installation process"""
    print("🚀 Sticky Note Organizer Installation")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Change to project directory
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies!")
        sys.exit(1)
    
    # Set up development environment
    if not setup_development_environment():
        print("❌ Failed to set up development environment!")
        sys.exit(1)
    
    # Create example files
    create_example_config()
    
    print("\n🎉 Installation completed successfully!")
    print("\n📚 Next steps:")
    print("1. Run 'sticky-organizer info' to check your database")
    print("2. Run 'sticky-organizer extract' to extract your notes")
    print("3. Run 'sticky-organizer --help' for all available commands")
    print("\n💡 Pro tip: Use 'sticky-organizer categories' to see all available categories")


if __name__ == "__main__":
    main()
