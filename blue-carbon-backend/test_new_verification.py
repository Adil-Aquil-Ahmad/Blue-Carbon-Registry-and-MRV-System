import requests
import json

def test_verification_new_evidence():
    """Test verification of the new evidence ID 3 with AI-calculated credits"""
    
    base_url = "http://127.0.0.1:8000"
    evidence_id = 2
    
    print(f"🔍 Testing verification of Evidence ID {evidence_id}")
    print("Expected: 250.08 AI-calculated credits")
    print("=" * 50)
    
    # Test verification
    verify_data = {
        "evidence_id": evidence_id,
        "mint_receipt": True,
        "receipt_token_uri": "",
        "mint_amount": 0  # Should use AI-calculated amount (350.0)
    }
    
    try:
        response = requests.post(f"{base_url}/verify", json=verify_data)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Verification successful!")
            print(f"Credits Issued: {result.get('credits_issued')}")
            print(f"Calculation Method: {result.get('calculation_method')}")
            print(f"Transaction Hash: {result.get('tx_hash')}")
            
            # Check if it used AI-calculated credits
            credits_issued = result.get('credits_issued')
            if credits_issued == 250:
                print("🎉 SUCCESS: Used AI-calculated credits (250)!")
            elif credits_issued == 100:
                print("❌ PROBLEM: Still using hardcoded 100 credits")
            elif credits_issued == 0:
                print("❌ PROBLEM: No credits issued (0)")
            else:
                print(f"⚠️  UNEXPECTED: Issued {credits_issued} credits")
                
            # Check project credits after verification
            projects_response = requests.get(f"{base_url}/projects")
            if projects_response.status_code == 200:
                projects = projects_response.json()
                if projects:
                    total_credits = projects[0].get('totalIssuedCredits', 0)
                    print(f"📊 Total project credits after verification: {total_credits}")
                    
        else:
            print(f"❌ Verification failed: {response.status_code}")
            print(f"Response: {response.text}")
            
            # Check if it's already verified
            if "Already verified" in response.text:
                print("💡 Evidence already verified on blockchain")
            elif "Evidence not found" in response.text:
                print("💡 Evidence not found - may need to check evidence ID")
                
    except requests.exceptions.ConnectionError:
        print("❌ Backend server not running. Start it with the system.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_verification_new_evidence()