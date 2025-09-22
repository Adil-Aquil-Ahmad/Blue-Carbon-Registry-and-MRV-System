import sqlite3

def reset_verification_status():
    """Reset verification status in database so we can re-verify with correct credits"""
    
    conn = sqlite3.connect('bluecarbon.db')
    cursor = conn.cursor()
    
    # Check current status
    cursor.execute("SELECT id, calculated_carbon_credits, verified, credit_calculation_method FROM mrvdata")
    records = cursor.fetchall()
    
    print("📊 Current MRV Data Status:")
    for record in records:
        print(f"  ID: {record[0]}, Credits: {record[1]}, Verified: {record[2]}, Method: {record[3]}")
    
    # Reset verification status to allow re-verification
    cursor.execute("UPDATE mrvdata SET verified = 0 WHERE verified = 1")
    conn.commit()
    
    print("\n🔄 Reset verification status in database")
    
    # Check updated status
    cursor.execute("SELECT id, calculated_carbon_credits, verified FROM mrvdata")
    updated_records = cursor.fetchall()
    
    print("📊 Updated MRV Data Status:")
    for record in updated_records:
        print(f"  ID: {record[0]}, Credits: {record[1]}, Verified: {record[2]}")
    
    total_credits = sum(record[1] for record in updated_records if record[1])
    print(f"\n💰 Total AI-calculated credits ready for verification: {total_credits}")
    
    conn.close()

if __name__ == "__main__":
    print("🔧 Resetting Verification Status")
    print("=" * 40)
    reset_verification_status()
    print("\n✅ Ready to re-verify with correct AI-calculated credits!")
    print("💡 Note: Blockchain may still show 'Already verified', but this allows testing the logic.")