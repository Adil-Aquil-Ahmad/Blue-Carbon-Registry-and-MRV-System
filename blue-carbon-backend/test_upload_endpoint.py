import requests
import os

# Test the upload endpoint directly
url = "http://127.0.0.1:8000/upload"

# Create test data
data = {
    'project_id': 2,  # Database project ID
    'uploader': 'test_user',
    'gps': '40.7128,-74.0060',
    'evidence_type': 'general',
    'project_area_hectares': 5.0,
    'time_period_years': 1.0
}

# Test with a simple text file
test_file_content = b"Test evidence content"
test_file_name = "test_evidence.txt"

files = {
    'files': (test_file_name, test_file_content, 'text/plain')
}

print("Testing upload endpoint...")
print(f"Data: {data}")

try:
    response = requests.post(url, data=data, files=files)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")