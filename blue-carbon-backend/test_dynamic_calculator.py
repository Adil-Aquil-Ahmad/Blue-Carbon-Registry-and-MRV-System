#!/usr/bin/env python3
"""
Test the DynamicCarbonCreditCalculator to find the exact error.
"""

import sys
import os
import traceback
from PIL import Image
import numpy as np

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.dynamic_carbon_credit_calculator import DynamicCarbonCreditCalculator

def create_simple_image(vegetation_percentage: float) -> bytes:
    """Create a simple test image."""
    width, height = 100, 100
    
    # Create base image (brown for soil)
    image = np.ones((height, width, 3), dtype=np.uint8)
    image[:, :, 0] = 139  # Red
    image[:, :, 1] = 119  # Green  
    image[:, :, 2] = 101  # Blue
    
    # Add vegetation (green pixels)
    total_pixels = width * height
    veg_pixels = int((vegetation_percentage / 100) * total_pixels)
    
    if veg_pixels > 0:
        for i in range(veg_pixels):
            y = i // width
            x = i % width
            if y < height:
                image[y, x, 0] = 30   # Low red
                image[y, x, 1] = 120  # High green
                image[y, x, 2] = 40   # Low blue
    
    # Convert to bytes
    from io import BytesIO
    pil_image = Image.fromarray(image)
    img_buffer = BytesIO()
    pil_image.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    return img_buffer.getvalue()

def test_dynamic_calculator():
    """Test the DynamicCarbonCreditCalculator exactly like the API does."""
    print("Testing DynamicCarbonCreditCalculator...")
    
    try:
        # Create calculator
        print("1. Creating DynamicCarbonCreditCalculator...")
        calculator = DynamicCarbonCreditCalculator()
        print("✓ Calculator created successfully")
        
        # Create test images
        print("2. Creating test images...")
        before_image_data = create_simple_image(10)  # 10% vegetation
        after_image_data = create_simple_image(60)   # 60% vegetation
        print("✓ Test images created")
        
        # Call the method exactly like the API does
        print("3. Calling calculate_dynamic_credits...")
        result = calculator.calculate_dynamic_credits(
            before_image_data=before_image_data,
            after_image_data=after_image_data,
            project_area_hectares=5.0,
            time_period_years=2.0,
            project_metadata={
                "ecosystem_type": "mangrove",
                "estimation_mode": True
            }
        )
        print("✓ calculate_dynamic_credits completed successfully")
        
        # Check the result
        if result.get('success'):
            print(f"✓ SUCCESS: {result.get('recommended_credits', 'N/A')} credits")
            print(f"  - Multiplier info: {result.get('supporting_analysis', {}).get('vegetation_change_multiplier', 'N/A')}")
        else:
            print(f"✗ FAILED: {result.get('error', 'Unknown error')}")
            
        return result
        
    except Exception as e:
        print(f"✗ ERROR: {str(e)}")
        print("\nFull traceback:")
        traceback.print_exc()
        return None

if __name__ == "__main__":
    test_dynamic_calculator()