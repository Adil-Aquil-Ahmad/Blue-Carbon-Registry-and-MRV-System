#!/usr/bin/env python3
"""
Test the actual API endpoint with before/after images to verify the vegetation multiplier integration.
"""

import requests
import io
from PIL import Image
import numpy as np
import json

def create_test_image(vegetation_coverage: float, size: tuple = (400, 300)) -> io.BytesIO:
    """Create a synthetic test image with specified vegetation coverage percentage."""
    width, height = size
    
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
    
    # Convert to PIL Image and save to BytesIO
    pil_image = Image.fromarray(image)
    image_buffer = io.BytesIO()
    pil_image.save(image_buffer, format='PNG')
    image_buffer.seek(0)
    
    return image_buffer

def test_api_endpoint():
    """Test the API endpoint with before/after images."""
    print("=" * 60)
    print("TESTING API ENDPOINT WITH VEGETATION MULTIPLIER")
    print("=" * 60)
    
    # Set random seed for reproducible results
    np.random.seed(42)
    
    # Create test images
    before_image = create_test_image(15)  # 15% vegetation (before)
    after_image = create_test_image(55)   # 55% vegetation (after) - should get ~1.5x multiplier
    
    # Prepare the request
    url = "http://localhost:8000/estimate-carbon-credits"
    
    files = {
        'before_image': ('before.png', before_image, 'image/png'),
        'after_image': ('after.png', after_image, 'image/png')
    }
    
    data = {
        'project_area_hectares': 5.0,
        'time_period_years': 2.0,
        'ecosystem_type': 'mangrove'
    }
    
    try:
        print(f"Sending request to {url}")
        print(f"Before image: 15% vegetation coverage")
        print(f"After image: 55% vegetation coverage") 
        print(f"Expected vegetation change: +40% (should get ~1.5x multiplier)")
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
            if 1.3 <= multiplier <= 1.5:
                print(f"\n✓ PASS: Multiplier {multiplier} is in expected range for large vegetation improvement")
            else:
                print(f"\n⚠ WARNING: Multiplier {multiplier} may be outside expected range (1.3-1.5)")
            
        else:
            print(f"✗ API Request failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("✗ ERROR: Could not connect to the API server.")
        print("Make sure the server is running on http://localhost:8000")
        print("Run: python main.py")
        
    except Exception as e:
        print(f"✗ ERROR: {str(e)}")

if __name__ == "__main__":
    test_api_endpoint()