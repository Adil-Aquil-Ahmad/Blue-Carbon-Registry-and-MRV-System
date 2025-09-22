import requests
import json

# Test the updated project system
base_url = "http://127.0.0.1:8000"

def test_projects_by_username():
    """Test if projects are filtered by username correctly"""
    
    print("🧪 Testing username-based project filtering...")
    
    try:
        # Test /projects endpoint
        response = requests.get(f'{base_url}/projects')
        if response.status_code == 200:
            projects = response.json()
            print(f"✅ Total projects: {len(projects)}")
            for project in projects:
                print(f"  - {project['name']} (Username: {project.get('username', 'N/A')})")
        else:
            print(f"❌ /projects failed: {response.status_code}")
            
        # Test /projects/my endpoint (this requires authentication)
        response = requests.get(f'{base_url}/projects/my')
        if response.status_code == 200:
            my_projects = response.json()
            print(f"✅ My projects: {len(my_projects)}")
        elif response.status_code == 401:
            print("ℹ️  /projects/my requires authentication (expected)")
        else:
            print(f"❌ /projects/my failed: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print('❌ Backend server not running. Start it with: python -m uvicorn main:app --reload --port 8000')
    except Exception as e:
        print(f'❌ Error: {e}')

def check_database_schema():
    """Check if username column was added to database"""
    import sqlite3
    
    try:
        conn = sqlite3.connect('bluecarbon.db')
        cursor = conn.cursor()
        
        cursor.execute("PRAGMA table_info(projects)")
        columns = [row[1] for row in cursor.fetchall()]
        
        if 'username' in columns:
            print("✅ Username column exists in projects table")
        else:
            print("❌ Username column missing from projects table")
            
        # Check current projects
        cursor.execute("SELECT name, username, owner FROM projects")
        projects = cursor.fetchall()
        print(f"✅ Projects in database: {len(projects)}")
        for project in projects:
            print(f"  - {project[0]} (Username: {project[1]}, Owner: {project[2]})")
            
        conn.close()
        
    except Exception as e:
        print(f"❌ Database error: {e}")

if __name__ == "__main__":
    print("🔍 Testing Username-Based Project System")
    print("=" * 50)
    
    check_database_schema()
    print()
    test_projects_by_username()