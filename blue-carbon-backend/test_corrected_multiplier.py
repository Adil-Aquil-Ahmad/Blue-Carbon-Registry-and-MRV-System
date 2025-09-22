def test_multiplier_calculation():
    """Test the corrected multiplier calculation logic"""
    
    # Data from Evidence 6
    before_vegetation = 0.0
    after_vegetation = 11.75524393717448
    
    print("🧮 Testing Corrected Multiplier Calculation:")
    print("=" * 50)
    print(f"Before vegetation coverage: {before_vegetation}%")
    print(f"After vegetation coverage: {after_vegetation}%")
    
    # Apply the new logic
    if before_vegetation < 5:  # Low starting vegetation
        vegetation_improvement = after_vegetation  # Use absolute improvement
        calculation_type = "absolute improvement (low starting vegetation)"
    else:
        vegetation_improvement = ((after_vegetation - before_vegetation) / before_vegetation) * 100
        calculation_type = "relative improvement"
    
    # Calculate multiplier
    green_multiplier = 1.0 + min(vegetation_improvement / 100.0, 0.5)  # Cap at 1.5x
    
    print(f"\n📊 Calculation:")
    print(f"   Method: {calculation_type}")
    print(f"   Vegetation improvement: {vegetation_improvement:.1f}%")
    print(f"   Multiplier: {green_multiplier:.2f}x")
    
    # Calculate credits
    base_credits = 700.0  # 10 hectares mangrove
    final_credits = base_credits * green_multiplier
    
    print(f"\n💰 Credit Calculation:")
    print(f"   Base credits: {base_credits}")
    print(f"   Multiplier: {green_multiplier:.2f}x")
    print(f"   Final credits: {final_credits:.1f}")
    
    # Check if this matches expectation
    if abs(green_multiplier - 1.1) < 0.05:
        print(f"\n✅ SUCCESS: Multiplier {green_multiplier:.2f} is close to expected 1.1")
    else:
        print(f"\n⚠️  RESULT: Multiplier {green_multiplier:.2f} (expected ~1.1)")
        
    print(f"\n📝 Explanation:")
    print(f"   - {after_vegetation:.1f}% vegetation coverage means {vegetation_improvement:.1f}% improvement")
    print(f"   - This gives a {green_multiplier:.2f}x multiplier")
    print(f"   - For exactly 1.1x, we'd need 10% improvement")

if __name__ == "__main__":
    test_multiplier_calculation()