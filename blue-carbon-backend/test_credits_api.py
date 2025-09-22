import requests

def test_credits_api():
    """Test if the API now returns correct credits"""
    
    try:
        response = requests.get("http://127.0.0.1:8000/projects")
        
        if response.status_code == 200:
            projects = response.json()
            if projects:
                project = projects[0]
                credits = project.get('totalIssuedCredits', 0)
                print(f"✅ Project: {project.get('name')}")
                print(f"✅ Total Issued Credits: {credits}")
                
                if credits == 850.1643830857145:
                    print("🎉 SUCCESS: Frontend will now show correct credits!")
                elif credits == 0:
                    print("❌ STILL ZERO: Credits not updated")
                else:
                    print(f"⚠️  UNEXPECTED: Credits showing {credits}")
                    
            else:
                print("❌ No projects found")
        else:
            print(f"❌ API failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_credits_api()