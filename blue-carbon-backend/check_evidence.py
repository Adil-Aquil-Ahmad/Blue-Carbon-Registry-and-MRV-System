import sqlite3

def check_evidence_database():
    """Check the evidence database structure and records"""
    
    conn = sqlite3.connect('bluecarbon.db')
    cursor = conn.cursor()
    
    # Check table structure
    cursor.execute("PRAGMA table_info(evidence)")
    columns = cursor.fetchall()
    print("Evidence table columns:")
    for col in columns:
        print(f"  - {col[1]} ({col[2]})")
    
    print()
    
    # Check evidence records
    cursor.execute("SELECT * FROM evidence")
    evidence = cursor.fetchall()
    print(f"Evidence records: {len(evidence)}")
    
    if evidence:
        for e in evidence:
            print(f"Evidence ID {e[0]}:")
            if len(e) > 1:
                print(f"  - Project ID: {e[1]}")
            if len(e) > 2:
                print(f"  - Image Path: {e[2]}")
            if len(e) > 3:
                print(f"  - Estimated Credits: {e[3]}")
            if len(e) > 4:
                print(f"  - Status: {e[4]}")
            if len(e) > 5:
                print(f"  - Analysis Results: {e[5]}")
            print()
    else:
        print("No evidence records found")
    
    conn.close()

if __name__ == "__main__":
    check_evidence_database()