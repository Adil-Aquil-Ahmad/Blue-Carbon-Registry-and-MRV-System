#!/usr/bin/env python3
"""
Test the greenness analyzer and API with actual images.
"""

import requests
import io
import numpy as np
from PIL import Image

def create_test_image_with_greenness(green_percentage: float, filename: str) -> str:
    """Create a test image with specified percentage of green pixels."""
    width, height = 400, 300
    
    # Create base brown/tan image (soil)
    image = np.ones((height, width, 3), dtype=np.uint8)
    image[:, :, 0] = 139  # Red
    image[:, :, 1] = 119  # Green  
    image[:, :, 2] = 101  # Blue
    
    # Add green vegetation pixels
    total_pixels = width * height
    green_pixels = int((green_percentage / 100) * total_pixels)
    
    if green_pixels > 0:
        # Random positions for green pixels
        green_positions = np.random.choice(total_pixels, green_pixels, replace=False)
        for pos in green_positions:
            y = pos // width
            x = pos % width
            # Create green vegetation pixel
            image[y, x, 0] = np.random.randint(20, 60)    # Low red
            image[y, x, 1] = np.random.randint(100, 180)  # High green
            image[y, x, 2] = np.random.randint(20, 80)    # Low blue
    
    # Save image
    pil_image = Image.fromarray(image)
    pil_image.save(filename, 'PNG')
    return filename

def test_greenness_api():
    """Test the API with before/after images containing different amounts of green."""
    print("🌱 Testing Greenness Analysis API")
    print("=" * 50)
    
    # Set seed for reproducible results
    np.random.seed(42)
    
    # Create test images
    before_file = create_test_image_with_greenness(15, 'before_test.png')  # 15% green
    after_file = create_test_image_with_greenness(60, 'after_test.png')    # 60% green - should get high multiplier
    
    print(f"📸 Created before image: 15% green pixels")
    print(f"📸 Created after image: 60% green pixels")
    print(f"📈 Expected: +45% green improvement → High multiplier")
    print("")
    
    # Test the API
    url = "http://127.0.0.1:8000/estimate-carbon-credits"
    
    try:
        with open(before_file, 'rb') as bf, open(after_file, 'rb') as af:
            files = {
                'before_image': ('before.png', bf, 'image/png'),
                'after_image': ('after.png', af, 'image/png')
            }
            
            data = {
                'project_area_hectares': 10.0,
                'time_period_years': 1.0,
                'ecosystem_type': 'mangrove'
            }
            
            print(f"🌐 Sending request to API...")
            response = requests.post(url, files=files, data=data, timeout=15)
            
            if response.status_code == 200:
                result = response.json()
                
                print("✅ API Request successful!")
                print("")
                print("📊 RESULTS:")
                print(f"   Estimation Type: {result.get('estimation_type', 'N/A')}")
                print(f"   Confidence Level: {result.get('confidence_level', 'N/A')}")
                print(f"   Estimated Credits: {result.get('estimated_credits', 'N/A')}")
                print(f"   CO₂ Sequestration: {result.get('co2_sequestration_kg', 'N/A')} kg")
                print(f"   Green Progress Multiplier: {result.get('green_progress_multiplier', 'N/A')}")
                print(f"   Green Progress Level: {result.get('green_progress_level', 'N/A')}")
                
                # Check greenness analysis
                greenness = result.get('greenness_analysis', {})
                if greenness:
                    print("")
                    print("🌱 GREENNESS ANALYSIS:")
                    print(f"   Before Green %: {greenness.get('before_green_percentage', 'N/A')}%")
                    print(f"   After Green %: {greenness.get('after_green_percentage', 'N/A')}%")
                    print(f"   Green Improvement: {greenness.get('green_improvement', 'N/A')}%")
                    print(f"   Justification: {greenness.get('multiplier_justification', 'N/A')}")
                
                # Check breakdown
                breakdown = result.get('breakdown', {})
                if breakdown:
                    print("")
                    print("💰 CALCULATION BREAKDOWN:")
                    for key, value in breakdown.items():
                        if 'green' in key.lower() or 'multiplier' in key.lower():
                            print(f"   {key.replace('_', ' ').title()}: {value}")
                
                # Verify expectations
                multiplier = result.get('green_progress_multiplier', 1.0)
                if multiplier >= 1.3:
                    print(f"\n✅ SUCCESS: High multiplier {multiplier:.2f}x achieved for significant green improvement!")
                elif multiplier >= 1.1:
                    print(f"\n✅ GOOD: Moderate multiplier {multiplier:.2f}x for green improvement")
                else:
                    print(f"\n⚠️  UNEXPECTED: Low multiplier {multiplier:.2f}x - expected higher for 45% improvement")
                
            else:
                print(f"❌ API Request failed: {response.status_code}")
                print(f"Response: {response.text}")
                
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Could not connect to API server")
        print("Make sure the server is running: python main.py")
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
    
    finally:
        # Clean up
        import os
        try:
            os.remove(before_file)
            os.remove(after_file)
        except:
            pass

if __name__ == "__main__":
    test_greenness_api()