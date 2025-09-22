import requests
import json

def test_verification():
    """Test the verification endpoint to see what credits are being assigned"""
    
    base_url = "http://127.0.0.1:8000"
    
    # Test the verification endpoint
    verify_data = {
        "evidence_id": 1,
        "mint_receipt": True,
        "receipt_token_uri": "",
        "mint_amount": 0
    }
    
    try:
        response = requests.post(f"{base_url}/verify", json=verify_data)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Verification successful!")
            print(f"Response: {json.dumps(result, indent=2)}")
        else:
            print(f"❌ Verification failed: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Backend server not running. Start it with: python -m uvicorn main:app --reload --port 8000")
    except Exception as e:
        print(f"❌ Error: {e}")

def check_current_credits():
    """Check current credits from project data"""
    
    base_url = "http://127.0.0.1:8000"
    
    try:
        # Check projects endpoint that includes totalIssuedCredits
        response = requests.get(f"{base_url}/projects")
        
        if response.status_code == 200:
            projects = response.json()
            if projects:
                project = projects[0]
                print(f"✅ Project: {project.get('name')}")
                print(f"✅ Total Issued Credits: {project.get('totalIssuedCredits', 'N/A')}")
                print(f"✅ Owner: {project.get('owner')}")
            else:
                print("No projects found")
        else:
            print(f"❌ Failed to get projects: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error checking credits: {e}")

if __name__ == "__main__":
    print("🔍 Testing Verification System")
    print("=" * 40)
    
    print("\n1. Checking current credits:")
    check_current_credits()
    
    print("\n2. Testing verification:")
    test_verification()