import requests

def check_evidence_details():
    """Check evidence 6 details"""
    
    try:
        response = requests.get("http://127.0.0.1:8000/debug/evidence/6")
        
        if response.status_code == 200:
            result = response.json()
            print("📊 Evidence 6 Details:")
            print(f"  Credits: {result.get('calculated_carbon_credits')}")
            print(f"  Method: {result.get('credit_calculation_method')}")
            print(f"  Confidence: {result.get('confidence_score')}")
            print(f"  Summary: {result.get('analysis_summary')}")
            print(f"  Verified: {result.get('verified')}")
            
            # Check if verification should work
            credits = result.get('calculated_carbon_credits')
            method = result.get('credit_calculation_method')
            confidence = result.get('confidence_score')
            
            if credits and method in ['ai_analysis', 'upload_page_calculation'] and confidence:
                print("✅ Evidence should be recognized by verification logic")
            else:
                print("❌ Evidence won't be recognized - missing criteria")
                print(f"   Credits: {credits is not None}")
                print(f"   Method: {method}")
                print(f"   Confidence: {confidence is not None}")
        else:
            print(f"❌ Failed to get evidence details: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_evidence_details()