#!/usr/bin/env python3
"""
Create green.png and red.png test images for testing the greenness analyzer.
"""

import numpy as np
from PIL import Image
import os

def create_test_images():
    """Create green and red test images"""
    width, height = 400, 300
    
    # Create GREEN image (high vegetation)
    print("🟢 Creating green.png (high vegetation image)...")
    green_image = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Fill with various shades of green
    for y in range(height):
        for x in range(width):
            # Create varied green vegetation
            green_value = np.random.randint(100, 200)  # High green values
            red_value = np.random.randint(20, 80)      # Low red values
            blue_value = np.random.randint(30, 100)    # Low blue values
            
            green_image[y, x, 0] = red_value   # R
            green_image[y, x, 1] = green_value # G  
            green_image[y, x, 2] = blue_value  # B
    
    # Save green image
    green_pil = Image.fromarray(green_image)
    green_pil.save("green.png")
    print(f"✅ Saved green.png ({width}x{height})")
    
    # Create RED/BROWN image (low/no vegetation - barren land)
    print("🟤 Creating red.png (barren land image)...")
    red_image = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Fill with brown/red soil colors (no vegetation)
    for y in range(height):
        for x in range(width):
            # Create brown/red soil tones
            red_value = np.random.randint(120, 180)    # High red values
            green_value = np.random.randint(80, 120)   # Medium green values
            blue_value = np.random.randint(60, 100)    # Lower blue values
            
            red_image[y, x, 0] = red_value   # R
            red_image[y, x, 1] = green_value # G
            red_image[y, x, 2] = blue_value  # B
    
    # Save red image
    red_pil = Image.fromarray(red_image)
    red_pil.save("red.png")
    print(f"✅ Saved red.png ({width}x{height})")
    
    print("")
    print("📊 Expected Analysis Results:")
    print("   Before (red.png): ~5-15% green pixels (barren land)")
    print("   After (green.png): ~80-95% green pixels (dense vegetation)")
    print("   Expected Multiplier: 1.4-1.5x (significant improvement)")
    print("")

def test_greenness_analysis():
    """Test the greenness analyzer with the created images"""
    print("🧪 Testing Greenness Analysis...")
    
    try:
        from services.greenness_analyzer import GreennessAnalyzer
        
        # Read the test images
        with open("red.png", "rb") as f:
            red_data = f.read()
        with open("green.png", "rb") as f:
            green_data = f.read()
        
        analyzer = GreennessAnalyzer()
        
        # Test individual greenness
        print("📸 Individual Greenness Analysis:")
        red_greenness = analyzer.calculate_greenness_percentage(red_data)
        green_greenness = analyzer.calculate_greenness_percentage(green_data)
        
        print(f"   Red image greenness: {red_greenness:.2f}%")
        print(f"   Green image greenness: {green_greenness:.2f}%")
        
        # Test full multiplier calculation (red = before, green = after)
        print("\n🔢 Full Multiplier Calculation:")
        result = analyzer.calculate_green_progress_multiplier(
            before_image_data=red_data,
            after_image_data=green_data
        )
        
        print(f"   Green Progress Multiplier: {result['green_progress_multiplier']:.3f}x")
        print(f"   Green Progress Level: {result['green_progress_level']}")
        print(f"   Before Green %: {result['before_green_percentage']:.2f}%")
        print(f"   After Green %: {result['after_green_percentage']:.2f}%")
        print(f"   Green Improvement: {result['green_improvement']:+.2f}%")
        print(f"   Confidence: {result['confidence_level']}")
        print(f"   Justification: {result['analysis_details']['justification']}")
        
        return result
        
    except Exception as e:
        print(f"❌ Error in greenness analysis: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    create_test_images()
    test_greenness_analysis()