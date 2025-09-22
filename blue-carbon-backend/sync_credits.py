import sqlite3

def sync_project_credits():
    """Sync project total_issued_credits with verified MRV data"""
    
    conn = sqlite3.connect('bluecarbon.db')
    cursor = conn.cursor()
    
    # Calculate total verified credits for each project
    cursor.execute("""
        SELECT project_id, SUM(calculated_carbon_credits) as total_credits
        FROM mrvdata 
        WHERE verified = 1 AND calculated_carbon_credits IS NOT NULL
        GROUP BY project_id
    """)
    
    project_credits = cursor.fetchall()
    
    print("📊 Syncing Project Credits with Verified Evidence:")
    
    for project_id, total_credits in project_credits:
        # Update project total
        cursor.execute(
            "UPDATE projects SET total_issued_credits = ? WHERE id = ?", 
            (total_credits, project_id)
        )
        
        # Get project name
        cursor.execute("SELECT name FROM projects WHERE id = ?", (project_id,))
        project_name = cursor.fetchone()[0]
        
        print(f"  ✅ Project {project_id} ({project_name}): {total_credits} credits")
    
    conn.commit()
    conn.close()
    
    print(f"\n🎉 Synced {len(project_credits)} projects with verified credits!")

if __name__ == "__main__":
    sync_project_credits()