import requests
import json
import os

def test_new_evidence_upload():
    """Test uploading new evidence and verifying with AI-calculated credits"""
    
    base_url = "http://127.0.0.1:8000"
    
    # Find an existing image file to upload
    uploads_dir = "uploads"
    if os.path.exists(uploads_dir):
        image_files = [f for f in os.listdir(uploads_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        if image_files:
            test_image = os.path.join(uploads_dir, image_files[0])
            print(f"📸 Using test image: {test_image}")
            
            # Upload evidence
            try:
                with open(test_image, 'rb') as file:
                    files = {'image': file}
                    data = {
                        'project_id': '1',
                        'gps': '40.7128,-74.0060',
                        'uploader': '0x8626f6940E2eb28930eFb4CeF49B2d1F2C9C1199'
                    }
                    
                    response = requests.post(f"{base_url}/upload-evidence", files=files, data=data)
                    
                    if response.status_code == 200:
                        result = response.json()
                        print("✅ Evidence uploaded successfully!")
                        print(f"Evidence ID: {result.get('evidence_id')}")
                        print(f"Recommended Credits: {result.get('recommended_credits', 'N/A')}")
                        
                        # Now test verification
                        evidence_id = result.get('evidence_id')
                        if evidence_id:
                            print(f"\n🔍 Testing verification of evidence {evidence_id}...")
                            
                            verify_data = {
                                "evidence_id": evidence_id,
                                "mint_receipt": True,
                                "receipt_token_uri": "",
                                "mint_amount": 0  # Should use AI-calculated amount
                            }
                            
                            verify_response = requests.post(f"{base_url}/verify", json=verify_data)
                            
                            if verify_response.status_code == 200:
                                verify_result = verify_response.json()
                                print("✅ Verification successful!")
                                print(f"Credits Issued: {verify_result.get('credits_issued')}")
                                print(f"Calculation Method: {verify_result.get('calculation_method')}")
                                print(f"Transaction Hash: {verify_result.get('tx_hash')}")
                            else:
                                print(f"❌ Verification failed: {verify_response.status_code}")
                                print(f"Response: {verify_response.text}")
                        
                    else:
                        print(f"❌ Evidence upload failed: {response.status_code}")
                        print(f"Response: {response.text}")
                        
            except Exception as e:
                print(f"❌ Error uploading evidence: {e}")
        else:
            print("❌ No image files found in uploads directory")
    else:
        print("❌ Uploads directory not found")

if __name__ == "__main__":
    print("🧪 Testing New Evidence Upload & Verification")
    print("=" * 50)
    test_new_evidence_upload()