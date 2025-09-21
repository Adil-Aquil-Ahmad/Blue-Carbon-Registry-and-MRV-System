#!/usr/bin/env python3
"""
Add Green Progress fields to the database.
"""

import sqlite3
import os

def add_green_progress_columns():
    """Add the missing Green Progress columns to the database."""
    db_path = "bluecarbon.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Database {db_path} not found!")
        return False
    
    print(f"🗃️  Adding Green Progress columns to {db_path}...")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # List of Green Progress columns to add
        columns_to_add = [
            ("green_progress_multiplier", "REAL DEFAULT 1.0"),
            ("green_progress_level", "TEXT"),
            ("before_green_percentage", "REAL"),
            ("after_green_percentage", "REAL"),
            ("green_improvement", "REAL")
        ]
        
        for column_name, column_def in columns_to_add:
            try:
                cursor.execute(f"ALTER TABLE mrvdata ADD COLUMN {column_name} {column_def}")
                print(f"  SUCCESS: Added column: {column_name}")
            except sqlite3.OperationalError as e:
                if "duplicate column name" in str(e).lower():
                    print(f"  INFO: Column already exists: {column_name}")
                else:
                    print(f"  ERROR: Error adding {column_name}: {e}")
        
        conn.commit()
        
        # Verify columns were added
        cursor.execute("PRAGMA table_info(mrvdata)")
        columns = cursor.fetchall()
        
        print(f"\n📊 Current table columns ({len(columns)} total):")
        green_columns_found = []
        for col in columns:
            column_name = col[1]
            if "green" in column_name.lower():
                green_columns_found.append(column_name)
                print(f"  🌱 {column_name}")
        
        print(f"\n✅ Found {len(green_columns_found)} Green Progress columns:")
        for col in green_columns_found:
            print(f"    - {col}")
        
        conn.close()
        
        if len(green_columns_found) >= 5:
            print(f"\nSUCCESS: Green Progress migration completed successfully!")
            return True
        else:
            print(f"\n⚠️  Some Green Progress columns may be missing.")
            return False
            
    except Exception as e:
        print(f"❌ Error during migration: {e}")
        return False

if __name__ == "__main__":
    success = add_green_progress_columns()
    if success:
        print("\n🚀 Database is ready! You can now:")
        print("   1. Test the API with green/red images")
        print("   2. See Green Progress multipliers in action")
        print("   3. View updated carbon credit calculations")
    else:
        print("\n❌ Migration failed. Please check the errors above.")