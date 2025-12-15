"""
Database detection and handling for Microsoft Sticky Notes
"""

import os
import sqlite3
import platform
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime


class StickyNotesDatabase:
    """Handle Microsoft Sticky Notes database operations"""
    
    def __init__(self):
        self.db_path = None
        self.connection = None
        
    def find_database(self) -> Optional[str]:
        """
        Automatically detect Microsoft Sticky Notes database
        Supports both modern (plum.sqlite) and classic versions
        """
        system = platform.system().lower()
        possible_paths = []
        
        if system == "windows":
            # Modern Sticky Notes (Windows 10/11)
            user_profile = os.environ.get('USERPROFILE', '')
            modern_paths = [
                os.path.join(user_profile, 'AppData', 'Local', 'Packages', 
                           'Microsoft.MicrosoftStickyNotes_8wekyb3d8bbwe', 
                           'LocalState', 'plum.sqlite'),
                # Alternative path for some Windows versions
                os.path.join(user_profile, 'AppData', 'Local', 'Packages',
                           'Microsoft.MicrosoftStickyNotes_8wekyb3d8bbwe',
                           'LocalState', 'Legacy', 'ThresholdNotes.snt'),
            ]
            possible_paths.extend(modern_paths)
            
            # Classic Sticky Notes (Windows 7/8/early 10)
            classic_paths = [
                os.path.join(user_profile, 'AppData', 'Roaming', 'Microsoft', 
                           'Sticky Notes', 'StickyNotes.snt'),
                os.path.join(user_profile, 'Documents', 'StickyNotes.snt'),
            ]
            possible_paths.extend(classic_paths)
            
        # Check current directory for manually placed databases
        current_dir_paths = [
            'plum.sqlite',
            'StickyNotes.snt',
            'ThresholdNotes.snt',
        ]
        possible_paths.extend(current_dir_paths)
        
        # Find the first existing database
        for path in possible_paths:
            if os.path.exists(path) and os.path.getsize(path) > 0:
                print(f"Found database: {path}")
                return path
                
        return None
    
    def connect(self, db_path: Optional[str] = None) -> bool:
        """Connect to the database"""
        if db_path:
            self.db_path = db_path
        else:
            self.db_path = self.find_database()
            
        if not self.db_path:
            return False
            
        try:
            self.connection = sqlite3.connect(self.db_path)
            return True
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            return False
    
    def get_table_info(self) -> Dict[str, List[str]]:
        """Get information about available tables and columns"""
        if not self.connection:
            return {}
            
        cursor = self.connection.cursor()
        tables = {}
        
        try:
            # Get all tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            table_names = [row[0] for row in cursor.fetchall()]
            
            # Get columns for each table
            for table in table_names:
                cursor.execute(f"PRAGMA table_info({table})")
                columns = [col[1] for col in cursor.fetchall()]
                tables[table] = columns
                
        except sqlite3.Error as e:
            print(f"Error getting table info: {e}")
            
        return tables
    
    def extract_notes(self) -> List[Dict[str, Any]]:
        """Extract all notes from the database"""
        if not self.connection:
            return []
            
        cursor = self.connection.cursor()
        notes = []
        
        try:
            # Check if Note table exists (modern format)
            tables = self.get_table_info()
            
            if 'Note' in tables:
                # Modern Sticky Notes format
                query = '''
                    SELECT Id, Text, CreatedAt, UpdatedAt, Theme, Type 
                    FROM Note 
                    WHERE DeletedAt IS NULL 
                    ORDER BY CreatedAt DESC
                '''
                cursor.execute(query)
                
                for row in cursor.fetchall():
                    note_id, text, created_at, updated_at, theme, note_type = row
                    
                    if text:
                        # Clean the text by removing ID prefixes
                        import re
                        clean_text = re.sub(r'\\id=[\w\-_]+\s*', '', text).strip()
                        
                        # Convert Windows file time to readable date
                        try:
                            if created_at:
                                unix_timestamp = (created_at - 116444736000000000) / 10000000
                                created_date = datetime.fromtimestamp(unix_timestamp).strftime('%Y-%m-%d %H:%M:%S')
                            else:
                                created_date = 'Unknown'
                        except:
                            created_date = str(created_at) if created_at else 'Unknown'
                            
                        try:
                            if updated_at:
                                unix_timestamp = (updated_at - 116444736000000000) / 10000000
                                updated_date = datetime.fromtimestamp(unix_timestamp).strftime('%Y-%m-%d %H:%M:%S')
                            else:
                                updated_date = created_date
                        except:
                            updated_date = str(updated_at) if updated_at else created_date
                        
                        notes.append({
                            'id': note_id or 'Unknown',
                            'content': clean_text,
                            'created_date': created_date,
                            'updated_date': updated_date,
                            'theme': theme or 'Default',
                            'type': note_type or 'Note'
                        })
            
            # TODO: Add support for classic Sticky Notes format
            # elif other_classic_table_exists:
            #     handle_classic_format()
                        
        except sqlite3.Error as e:
            print(f"Error extracting notes: {e}")
            
        return notes
    
    def close(self):
        """Close the database connection"""
        if self.connection:
            self.connection.close()
            self.connection = None