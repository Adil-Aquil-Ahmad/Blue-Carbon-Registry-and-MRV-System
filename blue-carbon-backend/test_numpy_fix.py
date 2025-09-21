#!/usr/bin/env python3

import numpy as np
import sys
import os

# Add the current directory to path so we can import from main.py
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import clean

def test_numpy_conversion():
    """Test that numpy types are properly converted to native Python types"""
    
    print("Testing numpy type conversion...")
    
    # Test numpy scalars
    test_cases = [
        ("numpy.bool", np.bool_(True)),
        ("numpy.float64", np.float64(3.14159)),
        ("numpy.int64", np.int64(42)),
        ("numpy.float32", np.float32(2.718)),
    ]
    
    for name, value in test_cases:
        try:
            result = clean(value)
            print(f"✓ {name}: {value} -> {result} (type: {type(result)})")
            assert isinstance(result, (bool, float, int)), f"Expected native type, got {type(result)}"
        except Exception as e:
            print(f"✗ {name}: Failed with error: {e}")
            return False
    
    # Test nested data structures with numpy types
    nested_data = {
        "analysis": {
            "success": np.bool_(True),
            "confidence": np.float64(0.85),
            "count": np.int64(100),
            "metrics": [np.float32(1.1), np.float32(2.2), np.float32(3.3)]
        }
    }
    
    try:
        result = clean(nested_data)
        print(f"✓ Nested structure conversion successful")
        print(f"  Original: {nested_data}")
        print(f"  Cleaned:  {result}")
        
        # Verify all types are native Python types
        assert isinstance(result["analysis"]["success"], bool)
        assert isinstance(result["analysis"]["confidence"], float)
        assert isinstance(result["analysis"]["count"], int)
        assert all(isinstance(x, float) for x in result["analysis"]["metrics"])
        
        print("✓ All numpy types successfully converted to native Python types")
        return True
        
    except Exception as e:
        print(f"✗ Nested structure test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_numpy_conversion()
    if success:
        print("\n🎉 All tests passed! Numpy serialization fix is working.")
    else:
        print("\n❌ Tests failed. Numpy serialization fix needs more work.")
    sys.exit(0 if success else 1)