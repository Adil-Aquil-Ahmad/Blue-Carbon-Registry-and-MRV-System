import requests

def test_upload_page_calculation():
    """Test the exact calculation used on the evidence upload page"""
    
    base_url = "http://127.0.0.1:8000"
    
    # Test the same parameters as your evidence
    data = {
        'project_area_hectares': 10.0,
        'time_period_years': 1.0,
        'ecosystem_type': 'mangrove'
    }
    
    try:
        response = requests.post(f"{base_url}/estimate-carbon-credits", data=data)
        
        if response.status_code == 200:
            result = response.json()
            
            print("🧮 Upload Page Credit Calculation:")
            print("=" * 40)
            print(f"📏 Project Area: {result.get('project_area_hectares')} hectares")
            print(f"🕒 Time Period: {result.get('time_period_years')} years") 
            print(f"🌿 Ecosystem: {result.get('ecosystem_type')}")
            print(f"💰 Estimated Credits: {result.get('estimated_credits')}")
            print(f"🌍 CO2 Sequestration: {result.get('co2_sequestration_kg')} kg")
            print(f"📊 Calculation Method: {result.get('calculation_method')}")
            
            if 'breakdown' in result:
                breakdown = result['breakdown']
                print(f"\n📋 Breakdown:")
                for key, value in breakdown.items():
                    print(f"   • {key}: {value}")
                    
            # This is what the upload page shows - this should match your expectation of 770
            print(f"\n💡 This is the credit amount shown on upload page: {result.get('estimated_credits')}")
            
        else:
            print(f"❌ Request failed: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_upload_page_calculation()