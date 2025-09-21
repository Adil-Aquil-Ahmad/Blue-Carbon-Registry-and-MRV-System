#!/usr/bin/env python3
"""
Test the image processing with actual files to debug the AI analysis issue.
"""

import sys
import os
import io
from PIL import Image
import numpy as np
import logging

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.ai_verification import BeforeAfterAnalyzer, NDVIAnalyzer

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def create_simple_test_image(vegetation_percentage: float, filename: str) -> str:
    """Create a simple test image file."""
    width, height = 200, 150
    
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
    
    # Save image
    pil_image = Image.fromarray(image)
    pil_image.save(filename, 'PNG')
    return filename

def test_image_analysis():
    """Test the image analysis step by step."""
    print("=" * 50)
    print("TESTING IMAGE ANALYSIS STEP BY STEP")
    print("=" * 50)
    
    try:
        # Create test images
        before_file = create_simple_test_image(10, 'debug_before.png')
        after_file = create_simple_test_image(60, 'debug_after.png')
        
        print(f"✓ Created test images: {before_file}, {after_file}")
        
        # Test NDVI analyzer first
        print("\n1. Testing NDVI Analyzer...")
        ndvi_analyzer = NDVIAnalyzer()
        
        with open(before_file, 'rb') as f:
            before_data = f.read()
        with open(after_file, 'rb') as f:
            after_data = f.read()
            
        print("✓ Image files read successfully")
        
        # Analyze individual images
        print("\n2. Analyzing before image...")
        before_analysis = ndvi_analyzer.analyze_image(before_data, "debug_before")
        
        if 'error' in before_analysis:
            print(f"✗ Before image analysis failed: {before_analysis['error']}")
            return False
        else:
            print(f"✓ Before image analysis successful")
            print(f"  - Vegetation coverage: {before_analysis.get('vegetation_analysis', {}).get('total_vegetation_coverage', 'N/A')}%")
            print(f"  - Mean NDVI: {before_analysis.get('ndvi_analysis', {}).get('mean_ndvi', 'N/A')}")
        
        print("\n3. Analyzing after image...")
        after_analysis = ndvi_analyzer.analyze_image(after_data, "debug_after")
        
        if 'error' in after_analysis:
            print(f"✗ After image analysis failed: {after_analysis['error']}")
            return False
        else:
            print(f"✓ After image analysis successful")
            print(f"  - Vegetation coverage: {after_analysis.get('vegetation_analysis', {}).get('total_vegetation_coverage', 'N/A')}%")
            print(f"  - Mean NDVI: {after_analysis.get('ndvi_analysis', {}).get('mean_ndvi', 'N/A')}")
        
        # Test BeforeAfterAnalyzer
        print("\n4. Testing BeforeAfterAnalyzer...")
        analyzer = BeforeAfterAnalyzer()
        
        print("\n5. Testing vegetation multiplier calculation...")
        multiplier_result = analyzer.calculate_vegetation_change_multiplier(before_analysis, after_analysis)
        
        print(f"✓ Vegetation multiplier calculation successful")
        print(f"  - Multiplier: {multiplier_result.get('vegetation_change_multiplier', 'N/A')}")
        print(f"  - Accuracy: {multiplier_result.get('accuracy_percentage', 'N/A')}%")
        print(f"  - Justification: {multiplier_result.get('analysis_details', {}).get('multiplier_justification', 'N/A')}")
        
        # Test full comparison
        print("\n6. Testing full before/after comparison...")
        comparison_result = analyzer.compare_images(
            before_data, after_data, 5.0, 1.0
        )
        
        if comparison_result.get('success'):
            print("✓ Full comparison successful")
            
            # Check vegetation multiplier in result
            veg_multiplier = comparison_result.get('vegetation_change_multiplier', {})
            if veg_multiplier:
                print(f"  - Vegetation multiplier: {veg_multiplier.get('vegetation_change_multiplier', 'N/A')}")
                print(f"  - Accuracy: {veg_multiplier.get('accuracy_percentage', 'N/A')}%")
            
            # Check CO2 results
            co2_results = comparison_result.get('co2_sequestration', {})
            if co2_results:
                print(f"  - Original CO2: {co2_results.get('original_co2_before_multiplier', 'N/A')} kg")
                print(f"  - Final CO2: {co2_results.get('co2_sequestration_kg', 'N/A')} kg")
                print(f"  - Multiplier applied: {co2_results.get('vegetation_change_multiplier_applied', 'N/A')}")
            
            # Check carbon credits
            credit_results = comparison_result.get('carbon_credits', {})
            if credit_results:
                print(f"  - Original credits: {credit_results.get('original_credits_before_multiplier', 'N/A')}")
                print(f"  - Final credits: {credit_results.get('carbon_credits', 'N/A')}")
            
            return True
        else:
            print(f"✗ Full comparison failed: {comparison_result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"✗ FATAL ERROR: {str(e)}")
        logger.exception("Fatal error in image analysis test")
        return False
    
    finally:
        # Clean up
        try:
            os.remove('debug_before.png')
            os.remove('debug_after.png')
        except:
            pass

if __name__ == "__main__":
    success = test_image_analysis()
    if success:
        print("\n🎉 All image analysis tests passed!")
    else:
        print("\n❌ Image analysis tests failed!")