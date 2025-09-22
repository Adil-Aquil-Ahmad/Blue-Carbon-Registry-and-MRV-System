#!/usr/bin/env python3
"""
Add username column to projects table
"""

import sqlite3
import os

def add_username_column():
    """Add username column to projects table"""
    db_path = "bluecarbon.db"
    
    if not os.path.exists(db_path):
        print("Database not found, it will be created when the server starts")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if username column already exists
        cursor.execute("PRAGMA table_info(projects)")
        columns = [row[1] for row in cursor.fetchall()]
        
        if 'username' not in columns:
            print("Adding username column to projects table...")
            cursor.execute("ALTER TABLE projects ADD COLUMN username TEXT")
            conn.commit()
            print("✅ Username column added successfully")
        else:
            print("✅ Username column already exists")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error updating database: {e}")

if __name__ == "__main__":
    add_username_column()