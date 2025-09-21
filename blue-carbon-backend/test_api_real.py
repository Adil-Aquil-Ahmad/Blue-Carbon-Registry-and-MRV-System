#!/usr/bin/env python3
"""
Test the actual API endpoint with real images to see the exact error.
"""

import requests
import os

def test_api_with_uploaded_images():
    """Test the API with the actual uploaded images"""
    print("🌐 Testing API with uploaded images")
    print("=" * 40)
    
    # Use uploaded images
    uploads_dir = "uploads"
    image_files = []
    
    if os.path.exists(uploads_dir):
        for file in os.listdir(uploads_dir):
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_files.append(os.path.join(uploads_dir, file))
    
    if len(image_files) < 2:
        print("❌ Need at least 2 images in uploads folder")
        return
    
    before_image_path = image_files[0]
    after_image_path = image_files[1]
    
    print(f"📷 Using before: {before_image_path}")
    print(f"📷 Using after: {after_image_path}")
    print("")
    
    url = "http://127.0.0.1:8000/estimate-carbon-credits"
    
    try:
        with open(before_image_path, 'rb') as bf, open(after_image_path, 'rb') as af:
            files = {
                'before_image': ('before.png', bf, 'image/png'),
                'after_image': ('after.png', af, 'image/png')
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
                print("📊 KEY FIELDS:")
                print(f"   Estimation Type: {result.get('estimation_type', 'N/A')}")
                print(f"   Calculation Method: {result.get('calculation_method', 'N/A')}")
                print(f"   Estimated Credits: {result.get('estimated_credits', 'N/A')}")
                print(f"   CO₂ Sequestration: {result.get('co2_sequestration_kg', 'N/A')} kg")
                print(f"   Confidence Level: {result.get('confidence_level', 'N/A')}")
                
                # Check for greenness fields
                print("")
                print("🌱 GREENNESS FIELDS:")
                print(f"   Green Progress Multiplier: {result.get('green_progress_multiplier', 'MISSING')}")
                print(f"   Green Progress Level: {result.get('green_progress_level', 'MISSING')}")
                
                greenness = result.get('greenness_analysis', {})
                if greenness:
                    print(f"   Before Green %: {greenness.get('before_green_percentage', 'N/A')}%")
                    print(f"   After Green %: {greenness.get('after_green_percentage', 'N/A')}%")
                    print(f"   Green Improvement: {greenness.get('green_improvement', 'N/A')}%")
                else:
                    print("   Greenness Analysis: MISSING")
                
                # Check for errors/warnings
                if 'warnings' in result:
                    print("")
                    print("⚠️  WARNINGS:")
                    for warning in result['warnings']:
                        print(f"   {warning}")
                
                if 'greenness_error' in result:
                    print("")
                    print("❌ GREENNESS ERROR:")
                    print(f"   {result['greenness_error']}")
                
                # Show breakdown
                breakdown = result.get('breakdown', {})
                if breakdown:
                    print("")
                    print("💰 BREAKDOWN:")
                    for key, value in breakdown.items():
                        print(f"   {key}: {value}")
                
            else:
                print(f"❌ API Error: {response.status_code}")
                print(f"Response: {response.text[:500]}")
                
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Could not connect to API server")
        print("Make sure the server is running on port 8000")
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")

if __name__ == "__main__":
    test_api_with_uploaded_images()