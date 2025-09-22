import requests

def test_latest_verification():
    """Test verification of the latest evidence"""
    
    base_url = "http://127.0.0.1:8000"
    
    # Test verification of Evidence ID 6 (latest unverified)
    evidence_id = 6
    
    verify_data = {
        "evidence_id": evidence_id,
        "mint_receipt": True,
        "receipt_token_uri": "",
        "mint_amount": 0  # Should use AI-calculated amount
    }
    
    try:
        print(f"🔍 Testing verification of Evidence ID {evidence_id}")
        print("Expected: 1400 credits (upload page calculation)")
        
        response = requests.post(f"{base_url}/verify", json=verify_data)
        
        if response.status_code == 200:
            result = response.json()
            credits_issued = result.get('credits_issued')
            
            print(f"✅ Verification Response:")
            print(f"   Credits Issued: {credits_issued}")
            print(f"   Calculation Method: {result.get('calculation_method')}")
            print(f"   Transaction Hash: {result.get('tx_hash')}")
            
            if credits_issued == 1400:
                print("🎉 SUCCESS: Correct credits issued!")
            elif credits_issued == 100:
                print("❌ PROBLEM: Still using hardcoded 100 credits")
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
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_latest_verification()