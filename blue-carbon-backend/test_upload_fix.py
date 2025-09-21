#!/usr/bin/env python3
"""
Test script to verify the upload endpoint fix for missing CO2 field
"""

import requests
import io

def test_upload_without_co2():
    """Test uploading evidence without the CO2 field (should now work)"""
    
    url = "http://localhost:8000/upload"
    
    # Create a test file in memory
    test_file_content = b"test file content"
    test_file = io.BytesIO(test_file_content)
    
    # Prepare form data (without CO2 field)
    files = {
        'files': ('test.txt', test_file, 'text/plain')
    }
    
    data = {
        'project_id': 1,
        'uploader': 'test_user',
        'gps': '40.7128,-74.0060',
        'evidence_type': 'general',
        'project_area_hectares': 10.0,
        'time_period_years': 1.0
        # Note: No 'co2' field - this should now work!
    }
    
    try:
        print("🧪 Testing upload without CO2 field...")
        response = requests.post(url, data=data, files=files, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("✅ SUCCESS: Upload worked without CO2 field!")
            return True
        else:
            print(f"❌ FAILED: {response.status_code} - {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed - make sure backend is running on localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_upload_with_co2():
    """Test uploading evidence with the CO2 field (should still work)"""
    
    url = "http://localhost:8000/upload"
    
    # Create a test file in memory
    test_file_content = b"test file content with co2"
    test_file = io.BytesIO(test_file_content)
    
    # Prepare form data (with CO2 field)
    files = {
        'files': ('test_with_co2.txt', test_file, 'text/plain')
    }
    
    data = {
        'project_id': 1,
        'uploader': 'test_user_with_co2',
        'gps': '40.7128,-74.0060',
        'co2': 500.0,  # Including CO2 field
        'evidence_type': 'general',
        'project_area_hectares': 10.0,
        'time_period_years': 1.0
    }
    
    try:
        print("\n🧪 Testing upload with CO2 field...")
        response = requests.post(url, data=data, files=files, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("✅ SUCCESS: Upload worked with CO2 field!")
            return True
        else:
            print(f"❌ FAILED: {response.status_code} - {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed - make sure backend is running on localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Testing Upload Endpoint Fix - CO2 Field Optional")
    print("=" * 60)
    
    # Test both scenarios
    test1_passed = test_upload_without_co2()
    test2_passed = test_upload_with_co2()
    
    print("\n" + "=" * 60)
    print("SUMMARY:")
    print(f"Upload without CO2: {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"Upload with CO2:    {'✅ PASSED' if test2_passed else '❌ FAILED'}")
    
    if test1_passed and test2_passed:
        print("\n🎉 All tests passed! The upload endpoint fix is working correctly.")
    else:
        print("\n⚠️ Some tests failed. Check the error messages above.")
    print("=" * 60)