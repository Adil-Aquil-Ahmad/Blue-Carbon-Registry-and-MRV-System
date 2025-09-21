#!/usr/bin/env python3
"""
Test the API with green.png and red.png to verify carbon credit calculation.
"""

import requests
import os

def test_api_with_green_red_images():
    """Test the API with red (before) and green (after) images"""
    print("🌐 Testing Carbon Credit API with Green/Red Images")
    print("=" * 55)
    
    # Check if images exist
    if not os.path.exists("red.png") or not os.path.exists("green.png"):
        print("❌ Images not found. Run create_test_images.py first")
        return
    
    print("📷 Using red.png as BEFORE image (barren land)")
    print("📷 Using green.png as AFTER image (dense vegetation)")
    print("📈 Expected: 1.5x multiplier for exceptional vegetation growth")
    print("")
    
    url = "http://127.0.0.1:8000/estimate-carbon-credits"
    
    try:
        with open("red.png", "rb") as before_f, open("green.png", "rb") as after_f:
            files = {
                'before_image': ('red.png', before_f, 'image/png'),
                'after_image': ('green.png', after_f, 'image/png')
            }
            
            data = {
                'project_area_hectares': 10.0,
                'time_period_years': 1.0,
                'ecosystem_type': 'mangrove'
            }
            
            print("🚀 Sending API request...")
            response = requests.post(url, files=files, data=data, timeout=15)
            
            if response.status_code == 200:
                result = response.json()
                
                print("✅ API Response received!")
                print("")
                print("📊 RESULTS:")
                print(f"   Estimation Type: {result.get('estimation_type', 'N/A')}")
                print(f"   Calculation Method: {result.get('calculation_method', 'N/A')}")
                print(f"   Confidence Level: {result.get('confidence_level', 'N/A')}")
                print("")
                print("💰 CARBON CALCULATIONS:")
                print(f"   Estimated Credits: {result.get('estimated_credits', 'N/A')}")
                print(f"   CO₂ Sequestration: {result.get('co2_sequestration_kg', 'N/A')} kg")
                
                # Check for greenness multiplier
                multiplier = result.get('green_progress_multiplier', 'MISSING')
                level = result.get('green_progress_level', 'MISSING')
                
                print("")
                print("🌱 GREENNESS ANALYSIS:")
                print(f"   Green Progress Multiplier: {multiplier}")
                print(f"   Green Progress Level: {level}")
                
                greenness = result.get('greenness_analysis', {})
                if greenness:
                    print(f"   Before Green %: {greenness.get('before_green_percentage', 'N/A')}%")
                    print(f"   After Green %: {greenness.get('after_green_percentage', 'N/A')}%")
                    print(f"   Green Improvement: {greenness.get('green_improvement', 'N/A')}%")
                    print(f"   Justification: {greenness.get('multiplier_justification', 'N/A')}")
                else:
                    print("   ❌ Greenness Analysis: NOT FOUND")
                
                # Expected vs Actual
                print("")
                print("📈 CALCULATION VERIFICATION:")
                baseline_co2 = 70000  # 7000 kg/ha * 10 ha
                baseline_credits = 700  # baseline_co2 * 10 * 0.001
                
                if multiplier != 'MISSING' and isinstance(multiplier, (int, float)):
                    expected_credits = baseline_credits * multiplier
                    expected_co2 = baseline_co2 * multiplier
                    
                    actual_credits = result.get('estimated_credits', 0)
                    actual_co2 = result.get('co2_sequestration_kg', 0)
                    
                    print(f"   Baseline Credits: {baseline_credits}")
                    print(f"   Expected Credits (with {multiplier}x): {expected_credits}")
                    print(f"   Actual Credits: {actual_credits}")
                    print(f"   Baseline CO₂: {baseline_co2} kg")
                    print(f"   Expected CO₂ (with {multiplier}x): {expected_co2} kg") 
                    print(f"   Actual CO₂: {actual_co2} kg")
                    
                    # Validation
                    credits_match = abs(actual_credits - expected_credits) < 1
                    co2_match = abs(actual_co2 - expected_co2) < 100
                    
                    if credits_match and co2_match:
                        print("   ✅ CALCULATIONS CORRECT!")
                    else:
                        print("   ❌ CALCULATION MISMATCH!")
                else:
                    print("   ❌ Multiplier not applied - using baseline calculation")
                
                # Check for errors
                if 'warnings' in result:
                    print("")
                    print("⚠️  WARNINGS:")
                    for warning in result['warnings']:
                        print(f"   {warning}")
                
                if 'greenness_error' in result:
                    print("")
                    print("❌ GREENNESS ERROR:")
                    print(f"   {result['greenness_error']}")
                
            else:
                print(f"❌ API Error: {response.status_code}")
                print(f"Response: {response.text[:500]}")
                
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Could not connect to API server")
        print("Make sure the server is running: python main.py")
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")

if __name__ == "__main__":
    test_api_with_green_red_images()