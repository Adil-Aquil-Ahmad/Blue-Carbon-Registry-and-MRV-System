import sqlite3
import json

def analyze_ai_calculations():
    """Analyze the AI calculation details stored in the database"""
    
    conn = sqlite3.connect('bluecarbon.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, project_area_hectares, calculated_carbon_credits, 
               green_progress_multiplier, ai_analysis_results, 
               calculated_co2_sequestration, vegetation_change_percentage,
               green_improvement, confidence_score
        FROM mrvdata 
        ORDER BY id
    """)
    
    records = cursor.fetchall()
    
    print("🔍 Detailed AI Analysis Breakdown:")
    print("=" * 60)
    
    for record in records:
        evidence_id = record[0]
        hectares = record[1]
        final_credits = record[2]
        multiplier = record[3]
        ai_results_json = record[4]
        co2_sequestration = record[5]
        vegetation_change = record[6]
        green_improvement = record[7]
        confidence = record[8]
        
        print(f"\n📋 Evidence ID {evidence_id}:")
        print(f"   📏 Area: {hectares} hectares")
        print(f"   💰 Final Credits: {final_credits}")
        print(f"   📈 Multiplier: {multiplier}")
        print(f"   🌱 CO2 Sequestration: {co2_sequestration}")
        print(f"   🍃 Vegetation Change: {vegetation_change}%")
        print(f"   📊 Green Improvement: {green_improvement}")
        print(f"   🎯 Confidence: {confidence}%")
        
        # Parse AI analysis results
        if ai_results_json:
            try:
                ai_results = json.loads(ai_results_json)
                print(f"   🤖 AI Analysis Details:")
                for key, value in ai_results.items():
                    if isinstance(value, (int, float)):
                        print(f"      - {key}: {value}")
                    elif isinstance(value, str) and len(value) < 100:
                        print(f"      - {key}: {value}")
                        
                # Look for any credit calculations in the AI results
                if 'credits' in str(ai_results_json).lower():
                    print(f"   💡 Credit mentions in AI results found!")
                    
            except json.JSONDecodeError:
                print(f"   ⚠️  AI results not valid JSON")
        
        # Manual calculation check
        if hectares and multiplier:
            expected_base = hectares * 77  # Base calculation (77 credits per hectare)
            expected_with_multiplier = expected_base * multiplier
            print(f"   🧮 Manual Check:")
            print(f"      - Base ({hectares} × 77): {expected_base}")
            print(f"      - With multiplier ({expected_base} × {multiplier}): {expected_with_multiplier}")
            
            if abs(final_credits - expected_with_multiplier) > 1:
                print(f"   ❌ MISMATCH: Expected {expected_with_multiplier}, got {final_credits}")
            else:
                print(f"   ✅ MATCHES calculation")
    
    conn.close()

if __name__ == "__main__":
    analyze_ai_calculations()