import sqlite3

# Check users and update existing project with a username
def update_existing_project():
    conn = sqlite3.connect('bluecarbon.db')
    cursor = conn.cursor()
    
    # Check if there are any users
    cursor.execute("SELECT id, username, wallet_address FROM users")
    users = cursor.fetchall()
    print(f"Users in database: {len(users)}")
    
    if users:
        for user in users:
            print(f"  - User ID: {user[0]}, Username: {user[1]}, Wallet: {user[2]}")
        
        # Update the existing project to use the first user's username
        first_user = users[0]
        cursor.execute("UPDATE projects SET username = ? WHERE username IS NULL", (first_user[1],))
        conn.commit()
        print(f"✅ Updated existing projects to use username: {first_user[1]}")
    else:
        print("No users found. Let's create a test user.")
        
        # Create a test user
        import hashlib
        
        password_hash = hashlib.sha256("test123".encode()).hexdigest()
        cursor.execute("""
            INSERT INTO users (username, email, password_hash, role, organization_name, wallet_address)
            VALUES (?, ?, ?, ?, ?, ?)
        """, ("testuser", "test@example.com", password_hash, "user", "Test Org", "0x8626f6940E2eb28930eFb4CeF49B2d1F2C9C1199"))
        
        conn.commit()
        print("✅ Created test user: testuser")
        
        # Update existing project
        cursor.execute("UPDATE projects SET username = ? WHERE username IS NULL", ("testuser",))
        conn.commit()
        print("✅ Updated existing projects to use username: testuser")
    
    # Verify the update
    cursor.execute("SELECT name, username, owner FROM projects")
    projects = cursor.fetchall()
    print(f"\nUpdated projects:")
    for project in projects:
        print(f"  - {project[0]} (Username: {project[1]}, Owner: {project[2]})")
    
    conn.close()

if __name__ == "__main__":
    update_existing_project()