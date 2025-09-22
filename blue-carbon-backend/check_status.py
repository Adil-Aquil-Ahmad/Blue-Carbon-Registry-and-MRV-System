import sqlite3

def check_verification_status():
    """Check verification status and credit totals"""
    
    conn = sqlite3.connect('bluecarbon.db')
    cursor = conn.cursor()
    
    # Check evidence 3 status
    cursor.execute("SELECT id, calculated_carbon_credits, verified FROM mrvdata WHERE id = 3")
    record = cursor.fetchone()
    if record:
        print(f"Evidence 3 status: Credits: {record[1]}, Verified: {record[2]}")
    else:
        print("Evidence 3 not found")
    
    # Check project total credits in database
    cursor.execute("SELECT total_issued_credits FROM projects WHERE id = 1")
    project = cursor.fetchone()
    if project:
        print(f"Project total credits in DB: {project[0]}")
    else:
        print("Project not found")
    
    # Check all verified evidence
    cursor.execute("SELECT id, calculated_carbon_credits, verified FROM mrvdata WHERE verified = 1")
    verified = cursor.fetchall()
    total_verified_credits = sum(r[1] for r in verified if r[1])
    print(f"All verified evidence: {len(verified)} records, {total_verified_credits} total credits")
    
    conn.close()

if __name__ == "__main__":
    check_verification_status()