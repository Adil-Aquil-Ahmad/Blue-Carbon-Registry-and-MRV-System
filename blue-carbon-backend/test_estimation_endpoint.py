"""
Test script for the carbon credit estimation endpoint
This demonstrates how the frontend can call the estimation API
"""

import requests
import json
from pathlib import Path

# API base URL
BASE_URL = "http://localhost:8000"

def test_basic_estimation():
    """Test basic estimation without images"""
    print("🧪 Testing basic carbon credit estimation...")
    
    data = {
        "project_area_hectares": 5.0,
        "time_period_years": 1.0,
        "ecosystem_type": "mangrove"
    }
    
    response = requests.post(f"{BASE_URL}/estimate-carbon-credits", data=data)
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Basic estimation successful!")
        print(f"   📏 Area: {result['project_area_hectares']} hectares")
        print(f"   🌱 Ecosystem: {result['ecosystem_type']}")
        print(f"   💰 Estimated Credits: {result['estimated_credits']}")
        print(f"   🌿 CO₂ Sequestration: {result['co2_sequestration_kg']} kg")
        print(f"   📊 Confidence: {result['confidence_level']}")
        print()
        return True
    else:
        print(f"❌ Basic estimation failed: {response.status_code}")
        print(response.text)
        return False

def test_ai_estimation_with_sample_images():
    """Test AI estimation with sample images"""
    print("🤖 Testing AI-enhanced estimation with images...")
    
    # Look for sample images in uploads directory
    uploads_dir = Path("uploads")
    if not uploads_dir.exists():
        print("⚠️ No uploads directory found. Skipping AI estimation test.")
        return False
    
    image_files = list(uploads_dir.glob("*.png")) + list(uploads_dir.glob("*.jpg"))
    
    if len(image_files) < 2:
        print("⚠️ Need at least 2 images in uploads directory. Skipping AI estimation test.")
        return False
    
    # Use first two images as before/after
    before_image = image_files[0]
    after_image = image_files[1]
    
    print(f"   📷 Before image: {before_image.name}")
    print(f"   📷 After image: {after_image.name}")
    
    data = {
        "project_area_hectares": 3.5,
        "time_period_years": 2.0,
        "ecosystem_type": "seagrass"
    }
    
    files = {
        "before_image": (before_image.name, open(before_image, "rb"), "image/png"),
        "after_image": (after_image.name, open(after_image, "rb"), "image/png")
    }
    
    try:
        response = requests.post(f"{BASE_URL}/estimate-carbon-credits", data=data, files=files)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ AI estimation successful!")
            print(f"   📏 Area: {result['project_area_hectares']} hectares")
            print(f"   🌱 Ecosystem: {result['ecosystem_type']}")
            print(f"   💰 Estimated Credits: {result['estimated_credits']}")
            print(f"   🌿 CO₂ Sequestration: {result['co2_sequestration_kg']} kg")
            print(f"   📊 Confidence: {result['confidence_level']}")
            print(f"   🔬 Method: {result['calculation_method']}")
            
            if 'ai_analysis' in result:
                ai = result['ai_analysis']
                print(f"   🌿 Vegetation Change: {ai['vegetation_change']:.1f}%")
                print(f"   📈 NDVI Improvement: {ai['ndvi_improvement']:.3f}")
                print(f"   🎯 AI Confidence: {ai['confidence_score']:.2f}")
            
            print()
            return True
        else:
            print(f"❌ AI estimation failed: {response.status_code}")
            print(response.text)
            return False
    
    finally:
        # Close file handles
        for file_tuple in files.values():
            if hasattr(file_tuple[1], 'close'):
                file_tuple[1].close()

def test_different_ecosystems():
    """Test estimation for different ecosystem types"""
    print("🌍 Testing different ecosystem types...")
    
    ecosystems = ["mangrove", "seagrass", "saltmarsh", "mixed"]
    area = 2.0
    
    for ecosystem in ecosystems:
        data = {
            "project_area_hectares": area,
            "time_period_years": 1.0,
            "ecosystem_type": ecosystem
        }
        
        response = requests.post(f"{BASE_URL}/estimate-carbon-credits", data=data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"   🌱 {ecosystem.capitalize():>10}: {result['estimated_credits']:>6.1f} credits "
                  f"({result['co2_sequestration_kg']:>6.0f} kg CO₂)")
        else:
            print(f"   ❌ {ecosystem}: Failed")
    
    print()

def test_error_conditions():
    """Test error handling"""
    print("⚠️ Testing error conditions...")
    
    # Test invalid area
    response = requests.post(f"{BASE_URL}/estimate-carbon-credits", data={
        "project_area_hectares": -1.0,
        "ecosystem_type": "mangrove"
    })
    print(f"   Invalid area: {'✅' if response.status_code == 400 else '❌'}")
    
    # Test invalid ecosystem
    response = requests.post(f"{BASE_URL}/estimate-carbon-credits", data={
        "project_area_hectares": 1.0,
        "ecosystem_type": "invalid_ecosystem"
    })
    print(f"   Invalid ecosystem: {'✅' if response.status_code == 400 else '❌'}")
    
    print()

if __name__ == "__main__":
    print("🚀 Carbon Credit Estimation Endpoint Test")
    print("=" * 50)
    
    try:
        # Test server connectivity
        response = requests.get(f"{BASE_URL}/")
        if response.status_code != 200:
            print("❌ Server not running. Please start the FastAPI server first.")
            exit(1)
        
        print("✅ Server is running")
        print()
        
        # Run tests
        test_basic_estimation()
        test_ai_estimation_with_sample_images()
        test_different_ecosystems()
        test_error_conditions()
        
        print("🎉 All estimation tests completed!")
        print()
        print("💡 Frontend Integration Tips:")
        print("   • Call /estimate-carbon-credits before submission")
        print("   • Show estimated credits to users for preview")
        print("   • Include confidence level in UI")
        print("   • Upload both before/after images for best accuracy")
        print("   • Display breakdown information to explain calculation")
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Please ensure FastAPI is running on localhost:8000")
    except Exception as e:
        print(f"❌ Test failed: {e}")