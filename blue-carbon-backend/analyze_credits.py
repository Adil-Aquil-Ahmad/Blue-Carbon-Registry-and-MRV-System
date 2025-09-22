import requests
import json

def check_blockchain_state():
    """Check the actual blockchain state for the project"""
    
    base_url = "http://127.0.0.1:8000"
    
    try:
        # Get project details from blockchain
        response = requests.get(f"{base_url}/projects")
        
        if response.status_code == 200:
            projects = response.json()
            if projects:
                project = projects[0]
                print("🔍 Current Project State:")
                print(f"  - Project ID: {project.get('id')}")
                print(f"  - Name: {project.get('name')}")
                print(f"  - Owner: {project.get('owner')}")
                print(f"  - Total Issued Credits: {project.get('totalIssuedCredits')}")
                print(f"  - Blockchain ID: {project.get('blockchainId')}")
                
                # Check MRV data
                response2 = requests.get(f"{base_url}/projects/{project.get('id')}")
                if response2.status_code == 200:
                    project_details = response2.json()
                    mrv_data = project_details.get('mrvData', [])
                    print(f"\n📊 MRV Evidence Data ({len(mrv_data)} records):")
                    
                    total_ai_credits = 0
                    for mrv in mrv_data:
                        credits = mrv.get('calculated_carbon_credits', 0)
                        total_ai_credits += credits if credits else 0
                        print(f"  - Evidence {mrv.get('id')}: {credits} credits (Verified: {mrv.get('verified')})")
                    
                    print(f"\n💰 Credit Analysis:")
                    print(f"  - AI Calculated Total: {total_ai_credits}")
                    print(f"  - Blockchain Issued: {project.get('totalIssuedCredits')}")
                    print(f"  - Difference: {total_ai_credits - project.get('totalIssuedCredits', 0)}")
                    
                    if total_ai_credits != project.get('totalIssuedCredits', 0):
                        print("  ❌ MISMATCH: AI calculated credits don't match blockchain issued credits!")
                        print("  💡 This explains why 0 credits are showing - verification used wrong amount.")
                    else:
                        print("  ✅ Credits match between AI calculation and blockchain")
                        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_blockchain_state()