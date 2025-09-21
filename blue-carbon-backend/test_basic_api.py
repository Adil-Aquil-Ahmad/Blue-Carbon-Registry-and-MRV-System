#!/usr/bin/env python3
"""
Simple test to verify the API endpoint is working and returning multiplier data.
"""

import requests
import json

def test_basic_api():
    """Test the API without images first."""
    print("Testing basic API endpoint...")
    
    url = "http://127.0.0.1:8000/estimate-carbon-credits"
    
    data = {
        'project_area_hectares': 5.0,
        'time_period_years': 2.0,
        'ecosystem_type': 'mangrove'
    }
    
    try:
        response = requests.post(url, data=data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print("✓ API Response successful!")
            print(f"Estimated Credits: {result.get('estimated_credits', 'N/A')}")
            print(f"Confidence Level: {result.get('confidence_level', 'N/A')}")
            print(f"Calculation Method: {result.get('calculation_method', 'N/A')}")
            
            # Check if the response structure is correct
            if 'estimated_credits' in result:
                print("✓ Basic API is working correctly")
                return True
            else:
                print("✗ API response missing expected fields")
                return False
        else:
            print(f"✗ API Request failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("✗ ERROR: Could not connect to the API server.")
        print("Make sure the server is running on http://127.0.0.1:8000")
        return False
        
    except Exception as e:
        print(f"✗ ERROR: {str(e)}")
        return False

if __name__ == "__main__":
    test_basic_api()