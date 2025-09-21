#!/usr/bin/env python3
"""
Test the full API with actual before/after images to verify multiplier integration.
"""

import requests
import io
from PIL import Image
import numpy as np

def create_test_image_file(vegetation_coverage: float, filename: str) -> str:
    """Create a test image file and save it."""
    width, height = 400, 300
    
    # Create base image (brown/tan for soil)
    image = np.ones((height, width, 3), dtype=np.uint8)
    image[:, :, 0] = 139  # Red channel - brown
    image[:, :, 1] = 119  # Green channel - brown  
    image[:, :, 2] = 101  # Blue channel - brown
    
    # Calculate how many pixels should be vegetation
    total_pixels = width * height
    vegetation_pixels = int((vegetation_coverage / 100) * total_pixels)
    
    if vegetation_pixels > 0:
        # Create random vegetation areas (green)
        vegetation_positions = np.random.choice(total_pixels, vegetation_pixels, replace=False)
        for pos in vegetation_positions:
            y = pos // width
            x = pos % width
            # Various shades of green for vegetation
            green_intensity = np.random.randint(80, 150)
            image[y, x, 0] = np.random.randint(20, 60)    # Low red
            image[y, x, 1] = green_intensity              # High green
            image[y, x, 2] = np.random.randint(20, 80)    # Low blue
    
    # Convert to PIL Image and save
    pil_image = Image.fromarray(image)
    pil_image.save(filename, 'PNG')
    return filename

def test_api_with_images():
    """Test the API with before/after images."""
    print("=" * 60)
    print("TESTING FULL API WITH BEFORE/AFTER IMAGES")
    print("=" * 60)
    
    # Set random seed for reproducible results
    np.random.seed(42)
    
    # Create test images
    before_file = create_test_image_file(15, 'test_before.png')  # 15% vegetation
    after_file = create_test_image_file(65, 'test_after.png')   # 65% vegetation - should get ~1.5x multiplier
    
    url = "http://127.0.0.1:8000/estimate-carbon-credits"
    
    # Prepare files and data
    with open(before_file, 'rb') as bf, open(after_file, 'rb') as af:
        files = {
            'before_image': ('before.png', bf, 'image/png'),
            'after_image': ('after.png', af, 'image/png')
        }
        
        data = {
            'project_area_hectares': 5.0,
            'time_period_years': 2.0,
            'ecosystem_type': 'mangrove'
        }
        
        try:
            print(f"Sending request to {url}")
            print(f"Before image: 15% vegetation coverage")
            print(f"After image: 65% vegetation coverage") 
            print(f"Expected vegetation change: +50% (should get ~1.5x multiplier)")
            print("")
            
            response = requests.post(url, files=files, data=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                
                print("✓ API Request successful!")
                print("")
                print("RESULTS:")
                print(f"• Estimation Type: {result.get('estimation_type', 'N/A')}")
                print(f"• Confidence Level: {result.get('confidence_level', 'N/A')}")
                print(f"• Estimated Credits: {result.get('estimated_credits', 'N/A')}")
                print(f"• CO2 Sequestration: {result.get('co2_sequestration_kg', 'N/A')} kg")
                print(f"• Vegetation Change Multiplier: {result.get('vegetation_change_multiplier', 'N/A')}")
                
                # Check AI analysis details
                ai_analysis = result.get('ai_analysis', {})
                if ai_analysis:
                    print(f"• Vegetation Change: {ai_analysis.get('vegetation_change', 'N/A')}%")
                    print(f"• NDVI Improvement: {ai_analysis.get('ndvi_improvement', 'N/A')}")
                    print(f"• Accuracy Percentage: {ai_analysis.get('accuracy_percentage', 'N/A')}%")
                    print(f"• Multiplier Justification: {ai_analysis.get('multiplier_justification', 'N/A')}")
                
                # Check breakdown details
                breakdown = result.get('breakdown', {})
                if breakdown:
                    print("")
                    print("BREAKDOWN:")
                    for key, value in breakdown.items():
                        print(f"• {key.replace('_', ' ').title()}: {value}")
                
                # Verify multiplier is reasonable
                multiplier = result.get('vegetation_change_multiplier', 1.0)
                if multiplier and 1.3 <= multiplier <= 1.5:
                    print(f"\n✓ PASS: Multiplier {multiplier} is in expected range for large vegetation improvement")
                elif multiplier:
                    print(f"\n⚠ WARNING: Multiplier {multiplier} may be outside expected range (1.3-1.5)")
                else:
                    print(f"\n✗ ERROR: No vegetation multiplier found in response")
                
                print(f"\n📝 Full API Response (first 500 chars):")
                print(str(result)[:500] + "..." if len(str(result)) > 500 else str(result))
                
            else:
                print(f"✗ API Request failed with status code: {response.status_code}")
                print(f"Response: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("✗ ERROR: Could not connect to the API server.")
            print("Make sure the server is running on http://127.0.0.1:8000")
            
        except Exception as e:
            print(f"✗ ERROR: {str(e)}")
    
    # Clean up test files
    import os
    try:
        os.remove(before_file)
        os.remove(after_file)
    except:
        pass

if __name__ == "__main__":
    test_api_with_images()