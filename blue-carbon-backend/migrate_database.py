"""
Database migration script for adding AI verification fields to MRVData table.
Run this script to update the existing database schema.
"""

import sqlite3
import os
from datetime import datetime

def migrate_database(db_path="bluecarbon.db"):
    """
    Add new fields to the MRVData table for AI verification support.
    """
    print(f"Starting database migration for {db_path}...")
    
    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='mrvdata';")
        if not cursor.fetchone():
            print("MRVData table not found. Creating new table with full schema...")
            create_new_table(cursor)
        else:
            print("MRVData table found. Adding new columns...")
            add_new_columns(cursor)
        
        # Commit changes
        conn.commit()
        print("Database migration completed successfully!")
        
        # Verify the migration
        verify_migration(cursor)
        
    except Exception as e:
        print(f"Migration failed: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

def create_new_table(cursor):
    """Create a new MRVData table with all fields."""
    create_table_sql = """
    CREATE TABLE mrvdata (
        id INTEGER PRIMARY KEY,
        project_id INTEGER,
        uploader TEXT,
        gps TEXT,
        co2 TEXT,
        media_hashes TEXT,
        evidence_hash TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        verified BOOLEAN DEFAULT 0,
        
        -- New AI verification fields
        evidence_type TEXT DEFAULT 'general',
        before_image_hash TEXT,
        after_image_hash TEXT,
        project_area_hectares REAL,
        
        -- AI Analysis Results
        calculated_co2_sequestration REAL,
        vegetation_change_percentage REAL,
        ndvi_improvement REAL,
        land_transformation_score REAL,
        
        -- Dynamic Carbon Credits
        calculated_carbon_credits REAL,
        credit_calculation_method TEXT DEFAULT 'ai_analysis',
        
        -- AI Analysis Metadata
        ai_analysis_results TEXT,
        confidence_score REAL,
        analysis_summary TEXT
    );
    """
    cursor.execute(create_table_sql)
    print("Created new MRVData table with AI verification fields")

def add_new_columns(cursor):
    """Add new columns to existing MRVData table."""
    new_columns = [
        "ALTER TABLE mrvdata ADD COLUMN evidence_type TEXT DEFAULT 'general';",
        "ALTER TABLE mrvdata ADD COLUMN before_image_hash TEXT;",
        "ALTER TABLE mrvdata ADD COLUMN after_image_hash TEXT;",
        "ALTER TABLE mrvdata ADD COLUMN project_area_hectares REAL;",
        "ALTER TABLE mrvdata ADD COLUMN calculated_co2_sequestration REAL;",
        "ALTER TABLE mrvdata ADD COLUMN vegetation_change_percentage REAL;",
        "ALTER TABLE mrvdata ADD COLUMN ndvi_improvement REAL;",
        "ALTER TABLE mrvdata ADD COLUMN land_transformation_score REAL;",
        "ALTER TABLE mrvdata ADD COLUMN calculated_carbon_credits REAL;",
        "ALTER TABLE mrvdata ADD COLUMN credit_calculation_method TEXT DEFAULT 'ai_analysis';",
        "ALTER TABLE mrvdata ADD COLUMN ai_analysis_results TEXT;",
        "ALTER TABLE mrvdata ADD COLUMN confidence_score REAL;",
        "ALTER TABLE mrvdata ADD COLUMN analysis_summary TEXT;"
    ]
    
    for sql in new_columns:
        try:
            cursor.execute(sql)
            column_name = sql.split("ADD COLUMN ")[1].split()[0]
            print(f"  ✓ Added column: {column_name}")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                column_name = sql.split("ADD COLUMN ")[1].split()[0]
                print(f"  - Column already exists: {column_name}")
            else:
                print(f"  ✗ Error adding column: {e}")

def verify_migration(cursor):
    """Verify that all new columns were added successfully."""
    cursor.execute("PRAGMA table_info(mrvdata);")
    columns = cursor.fetchall()
    
    expected_columns = [
        'evidence_type', 'before_image_hash', 'after_image_hash', 'project_area_hectares',
        'calculated_co2_sequestration', 'vegetation_change_percentage', 'ndvi_improvement',
        'land_transformation_score', 'calculated_carbon_credits', 'credit_calculation_method',
        'ai_analysis_results', 'confidence_score', 'analysis_summary'
    ]
    
    existing_columns = [col[1] for col in columns]
    
    print("\nVerification results:")
    for col in expected_columns:
        if col in existing_columns:
            print(f"  ✓ {col}")
        else:
            print(f"  ✗ Missing: {col}")
    
    print(f"\nTotal columns in table: {len(existing_columns)}")

if __name__ == "__main__":
    # Migrate main database
    db_path = "bluecarbon.db"
    if os.path.exists(db_path):
        migrate_database(db_path)
    else:
        print(f"Database file {db_path} not found. Will be created when application starts.")
    
    # Also migrate backend database if it exists
    backend_db_path = "blue-carbon-backend/bluecarbon.db"
    if os.path.exists(backend_db_path):
        print("\nMigrating backend database...")
        migrate_database(backend_db_path)
    
    print("\nMigration script completed!")
    print("\nNEXT STEPS:")
    print("1. Restart the FastAPI application")
    print("2. Test the new upload endpoint with evidence_type='before' or 'after'")
    print("3. Upload paired before/after images to see AI analysis in action")
    print("4. Use the /system/ai-verification-stats endpoint to monitor adoption")