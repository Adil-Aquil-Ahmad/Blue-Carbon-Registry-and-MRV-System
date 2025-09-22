import sqlite3
import json

def analyze_multiplier_calculation():
    """Analyze why the multiplier is 2.0 instead of 1.1"""
    
    conn = sqlite3.connect('bluecarbon.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, vegetation_change_percentage, green_progress_multiplier, 
               ai_analysis_results, analysis_summary
        FROM mrvdata 
        WHERE id = 6
    """)
    
    record = cursor.fetchone()
    
    if record:
        evidence_id = record[0]
        veg_change = record[1]
        multiplier = record[2]
        ai_results_json = record[3]
        summary = record[4]
        
        print(f"🔍 Evidence {evidence_id} Multiplier Analysis:")
        print(f"   Vegetation Change: {veg_change}%")
        print(f"   Calculated Multiplier: {multiplier}")
        print(f"   Summary: {summary}")
        
        if ai_results_json:
            try:
                ai_results = json.loads(ai_results_json)
                print(f"\n🤖 AI Analysis Results:")
                
                if 'supporting_analysis' in ai_results:
                    supporting = ai_results['supporting_analysis']
                    if 'transformation_metrics' in supporting:
                        metrics = supporting['transformation_metrics']
                        print(f"   Transformation Metrics:")
                        for key, value in metrics.items():
                            if isinstance(value, (int, float)):
                                print(f"      - {key}: {value}")
                
                # Look for greenness analysis
                if 'greenness_analysis' in ai_results:
                    greenness = ai_results['greenness_analysis']
                    print(f"   Greenness Analysis:")
                    for key, value in greenness.items():
                        if isinstance(value, (int, float)):
                            print(f"      - {key}: {value}")
                            
            except json.JSONDecodeError:
                print("   ⚠️  AI results not valid JSON")
        
        print(f"\n💡 Expected multiplier calculation:")
        print(f"   If 10% improvement → 1.0 + (10/100) = 1.1")
        print(f"   Current calculation → 1.0 + ({veg_change}/100) = {1.0 + (veg_change/100):.2f}")
        print(f"   But capped at 2.0, so result is {multiplier}")
        
        print(f"\n❌ Problem: {veg_change}% vegetation change is unrealistic!")
        print(f"   This should be around 10% for a 1.1 multiplier")
    
    conn.close()

if __name__ == "__main__":
    analyze_multiplier_calculation()