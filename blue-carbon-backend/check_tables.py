import sqlite3

def check_database_tables():
    """Check what tables exist in the database"""
    
    conn = sqlite3.connect('bluecarbon.db')
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    print("Tables in database:")
    for table in tables:
        print(f"  - {table[0]}")
        
        # Get table structure
        cursor.execute(f"PRAGMA table_info({table[0]})")
        columns = cursor.fetchall()
        for col in columns:
            print(f"    * {col[1]} ({col[2]})")
        
        # Get record count
        cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
        count = cursor.fetchone()[0]
        print(f"    Records: {count}")
        print()
    
    conn.close()

if __name__ == "__main__":
    check_database_tables()