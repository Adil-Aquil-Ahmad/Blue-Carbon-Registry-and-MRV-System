#!/usr/bin/env python3
"""
Test script for the vegetation change multiplier functionality.
Tests the new before/after image comparison and multiplier calculation.
"""

import sys
import os
import io
import logging
from PIL import Image
import numpy as np

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.ai_verification import BeforeAfterAnalyzer, NDVIAnalyzer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_test_image(vegetation_coverage: float, size: tuple = (400, 300)) -> bytes:
    """
    Create a synthetic test image with specified vegetation coverage percentage.
    
    Args:
        vegetation_coverage: Percentage of image that should be green (0-100)
        size: Image dimensions (width, height)
    
    Returns:
        Image data as bytes
    """
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
    
    # Convert to PIL Image and then to bytes
    pil_image = Image.fromarray(image)
    image_buffer = io.BytesIO()
    pil_image.save(image_buffer, format='PNG')
    image_buffer.seek(0)
    
    return image_buffer.getvalue()

def test_vegetation_multiplier():
    """Test the vegetation change multiplier calculation."""
    print("=" * 60)
    print("TESTING VEGETATION CHANGE MULTIPLIER SYSTEM")
    print("=" * 60)
    
    analyzer = BeforeAfterAnalyzer()
    
    # Test scenarios
    test_scenarios = [
        {"before": 5, "after": 60, "description": "Barren to Dense Forest (Should get ~1.5x)"},
        {"before": 20, "after": 45, "description": "Moderate Improvement (Should get ~1.2x)"},
        {"before": 30, "after": 35, "description": "Minimal Improvement (Should get ~1.0x)"},
        {"before": 40, "after": 40, "description": "No Change (Should get ~1.0x)"},
        {"before": 50, "after": 25, "description": "Significant Loss (Should get ~0.4x)"},
        {"before": 5, "after": 5, "description": "Barren Remains Barren (Should get 0.0x)"},
    ]
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n--- Test {i}: {scenario['description']} ---")
        print(f"Before vegetation: {scenario['before']}%")
        print(f"After vegetation: {scenario['after']}%")
        
        try:
            # Create test images
            before_image_data = create_test_image(scenario['before'])
            after_image_data = create_test_image(scenario['after'])
            
            # Analyze images individually first
            ndvi_analyzer = NDVIAnalyzer()
            before_analysis = ndvi_analyzer.analyze_image(before_image_data, "test_before")
            after_analysis = ndvi_analyzer.analyze_image(after_image_data, "test_after")
            
            # Calculate vegetation multiplier
            multiplier_result = analyzer.calculate_vegetation_change_multiplier(
                before_analysis, after_analysis
            )
            
            # Display results
            multiplier = multiplier_result['vegetation_change_multiplier']
            accuracy = multiplier_result['accuracy_percentage']
            details = multiplier_result.get('analysis_details', {})
            
            print(f"✓ Vegetation Change Multiplier: {multiplier:.3f}x")
            print(f"✓ Accuracy Percentage: {accuracy:.1f}%")
            print(f"✓ Justification: {details.get('multiplier_justification', 'N/A')}")
            print(f"✓ Detected vegetation change: {details.get('vegetation_change_percentage', 0):.1f}%")
            print(f"✓ NDVI improvement: {details.get('ndvi_improvement', 0):.3f}")
            
            # Verify multiplier is in expected range
            if scenario['description'].startswith("Barren to Dense"):
                expected_range = (1.3, 1.5)
            elif scenario['description'].startswith("Moderate"):
                expected_range = (1.1, 1.3)
            elif scenario['description'].startswith("Minimal") or scenario['description'].startswith("No Change"):
                expected_range = (0.9, 1.1)
            elif scenario['description'].startswith("Significant Loss"):
                expected_range = (0.3, 0.6)
            elif scenario['description'].startswith("Barren Remains"):
                expected_range = (0.0, 0.1)
            else:
                expected_range = (0.0, 1.5)
            
            if expected_range[0] <= multiplier <= expected_range[1]:
                print(f"✓ PASS: Multiplier {multiplier:.3f} is within expected range {expected_range}")
            else:
                print(f"✗ FAIL: Multiplier {multiplier:.3f} is outside expected range {expected_range}")
            
        except Exception as e:
            print(f"✗ ERROR: {str(e)}")
            logger.error(f"Error in test scenario {i}: {str(e)}")
    
    print(f"\n" + "=" * 60)
    print("TESTING COMPLETE")
    print("=" * 60)

def test_full_analysis():
    """Test the full before/after analysis with multiplier integration."""
    print(f"\n" + "=" * 60)
    print("TESTING FULL BEFORE/AFTER ANALYSIS")
    print("=" * 60)
    
    analyzer = BeforeAfterAnalyzer()
    
    # Create test images: before (barren) and after (forested)
    before_image_data = create_test_image(10)  # 10% vegetation
    after_image_data = create_test_image(70)   # 70% vegetation
    
    try:
        # Perform full analysis
        result = analyzer.compare_images(
            before_image_data=before_image_data,
            after_image_data=after_image_data,
            project_area_hectares=5.0,
            time_period_years=2.0
        )
        
        if result.get('success'):
            print("✓ Full analysis completed successfully")
            
            # Check if vegetation multiplier is included
            multiplier_info = result.get('vegetation_change_multiplier', {})
            if multiplier_info:
                print(f"✓ Vegetation Change Multiplier: {multiplier_info.get('vegetation_change_multiplier', 'N/A'):.3f}x")
                print(f"✓ Accuracy: {multiplier_info.get('accuracy_percentage', 'N/A'):.1f}%")
            
            # Check CO2 results
            co2_results = result.get('co2_sequestration', {})
            original_co2 = co2_results.get('original_co2_before_multiplier', 0)
            final_co2 = co2_results.get('co2_sequestration_kg', 0)
            multiplier_applied = co2_results.get('vegetation_change_multiplier_applied', 1.0)
            
            print(f"✓ Original CO2 (before multiplier): {original_co2:.1f} kg")
            print(f"✓ Final CO2 (after multiplier): {final_co2:.1f} kg")
            print(f"✓ Multiplier applied: {multiplier_applied:.3f}x")
            
            # Check carbon credits
            credit_results = result.get('carbon_credits', {})
            original_credits = credit_results.get('original_credits_before_multiplier', 0)
            final_credits = credit_results.get('carbon_credits', 0)
            
            print(f"✓ Original credits (before multiplier): {original_credits:.2f}")
            print(f"✓ Final credits (after multiplier): {final_credits:.2f}")
            
            print("\n✓ PASS: Full analysis integration working correctly")
            
        else:
            print(f"✗ FAIL: Analysis failed - {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"✗ ERROR: {str(e)}")
        logger.error(f"Error in full analysis test: {str(e)}")

if __name__ == "__main__":
    try:
        # Set random seed for reproducible test results
        np.random.seed(42)
        
        # Run tests
        test_vegetation_multiplier()
        test_full_analysis()
        
        print(f"\n🎉 All tests completed! Check results above.")
        
    except Exception as e:
        print(f"✗ FATAL ERROR: {str(e)}")
        logger.error(f"Fatal error in test execution: {str(e)}")
        sys.exit(1)