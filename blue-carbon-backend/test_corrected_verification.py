import requests

def verify_corrected_evidence():
    """Test verification of Evidence ID 7 with corrected calculation"""
    
    base_url = "http://127.0.0.1:8000"
    evidence_id = 7
    
    print("🔍 Testing Verification of Evidence ID 7")
    print("Expected: ~782 credits (corrected calculation)")
    print("=" * 50)
    
    # Test verification
    verify_data = {
        "evidence_id": evidence_id,
        "mint_receipt": True,
        "receipt_token_uri": "",
        "mint_amount": 0  # Should use calculated amount
    }
    
    try:
        response = requests.post(f"{base_url}/verify", json=verify_data)
        
        if response.status_code == 200:
            result = response.json()
            credits_issued = result.get('credits_issued')
            calculation_method = result.get('calculation_method')
            
            print("✅ Verification Response:")
            print(f"   Credits Issued: {credits_issued}")
            print(f"   Calculation Method: {calculation_method}")
            print(f"   Transaction Hash: {result.get('tx_hash')}")
            
            # Check if it used the correct amount
            if credits_issued == 782:
                print("🎉 SUCCESS: Used corrected credits (782)!")
            elif credits_issued == 100:
                print("❌ PROBLEM: Still using hardcoded 100 credits")
            elif credits_issued == 1400:
                print("❌ PROBLEM: Still using old incorrect calculation (1400)")
            else:
                print(f"⚠️  RESULT: Issued {credits_issued} credits")
                
            # Check total project credits
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
    verify_corrected_evidence()