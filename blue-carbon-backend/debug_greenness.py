#!/usr/bin/env python3
"""
Debug the greenness analyzer with the actual uploaded images.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))

from services.greenness_analyzer import GreennessAnalyzer
import traceback

def test_uploaded_images():
    """Test with the actual uploaded images from the uploads folder"""
    print("🔍 Testing Greenness Analyzer with uploaded images")
    print("=" * 55)
    
    # Look for the uploaded screenshots
    uploads_dir = "uploads"
    image_files = []
    
    if os.path.exists(uploads_dir):
        for file in os.listdir(uploads_dir):
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_files.append(os.path.join(uploads_dir, file))
    
    if len(image_files) < 2:
        print("❌ Need at least 2 images in uploads folder")
        return
    
    # Use the first two images
    before_image_path = image_files[0]
    after_image_path = image_files[1]
    
    print(f"📷 Before image: {before_image_path}")
    print(f"📷 After image: {after_image_path}")
    print("")
    
    try:
        # Read image data
        with open(before_image_path, 'rb') as f:
            before_data = f.read()
        with open(after_image_path, 'rb') as f:
            after_data = f.read()
        
        print(f"✅ Images loaded: Before={len(before_data)} bytes, After={len(after_data)} bytes")
        
        # Test greenness analyzer
        analyzer = GreennessAnalyzer()
        print("✅ GreennessAnalyzer initialized")
        
        # Test individual greenness calculation
        print("\n🌱 Testing individual greenness calculations...")
        before_greenness = analyzer.calculate_greenness_percentage(before_data)
        print(f"   Before greenness: {before_greenness:.2f}%")
        
        after_greenness = analyzer.calculate_greenness_percentage(after_data)
        print(f"   After greenness: {after_greenness:.2f}%")
        
        # Test full multiplier calculation
        print("\n🧮 Testing full multiplier calculation...")
        result = analyzer.calculate_green_progress_multiplier(
            before_image_data=before_data,
            after_image_data=after_data
        )
        
        print("✅ SUCCESS! Greenness analysis completed:")
        print(f"   Green Progress Multiplier: {result['green_progress_multiplier']:.3f}x")
        print(f"   Green Progress Level: {result['green_progress_level']}")
        print(f"   Before Green %: {result['before_green_percentage']:.2f}%")
        print(f"   After Green %: {result['after_green_percentage']:.2f}%")
        print(f"   Green Improvement: {result['green_improvement']:+.2f}%")
        print(f"   Confidence Level: {result['confidence_level']}")
        print(f"   Justification: {result['analysis_details']['justification']}")
        
    except Exception as e:
        print(f"❌ ERROR in greenness analysis: {str(e)}")
        print("\n🔍 Full traceback:")
        traceback.print_exc()

if __name__ == "__main__":
    test_uploaded_images()