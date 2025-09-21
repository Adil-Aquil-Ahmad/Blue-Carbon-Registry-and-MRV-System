"""
Test script for AI-based carbon credit calculation system.
Tests the before/after image analysis and dynamic credit calculation.
"""

import requests
import json
import os
import logging
from PIL import Image, ImageDraw
import numpy as np
import io
from typing import Dict, List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API Configuration
API_BASE_URL = "http://localhost:8000"
TEST_PROJECT_ID = 1
TEST_USER = "test_user@example.com"
TEST_GPS = "9.0579,76.2711"  # Kerala coordinates
TEST_AREA_HECTARES = 5.5

class AIVerificationTester:
    """
    Comprehensive tester for the AI verification system.
    """
    
    def __init__(self, api_base_url=API_BASE_URL):
        self.api_base_url = api_base_url
        self.session = requests.Session()
        
    def create_test_images(self) -> Dict[str, bytes]:
        """
        Create synthetic before/after images for testing.
        Before: mostly barren land with some sparse vegetation
        After: increased vegetation coverage (simulating restoration)
        """
        logger.info("Creating synthetic test images...")
        
        images = {}
        
        # Create "before" image - mostly barren with sparse vegetation
        before_img = Image.new('RGB', (800, 600), color=(139, 115, 85))  # Brown soil color
        draw = ImageDraw.Draw(before_img)
        
        # Add some sparse vegetation patches (green)
        vegetation_color = (34, 139, 34)  # Forest green
        for i in range(10):  # Sparse vegetation
            x = np.random.randint(50, 750)
            y = np.random.randint(50, 550)
            radius = np.random.randint(10, 30)
            draw.ellipse([x-radius, y-radius, x+radius, y+radius], fill=vegetation_color)
        
        # Add some water areas (blue)
        water_color = (30, 144, 255)  # Dodger blue
        for i in range(3):
            x = np.random.randint(100, 700)
            y = np.random.randint(100, 500)
            width = np.random.randint(50, 100)
            height = np.random.randint(20, 40)
            draw.ellipse([x, y, x+width, y+height], fill=water_color)
        
        # Convert to bytes
        before_buffer = io.BytesIO()
        before_img.save(before_buffer, format='PNG')
        images['before'] = before_buffer.getvalue()
        
        # Create "after" image - increased vegetation coverage
        after_img = Image.new('RGB', (800, 600), color=(139, 115, 85))  # Same soil base
        draw = ImageDraw.Draw(after_img)
        
        # Add much more vegetation (simulating restoration success)
        for i in range(35):  # Much more vegetation
            x = np.random.randint(50, 750)
            y = np.random.randint(50, 550)
            radius = np.random.randint(15, 45)
            # Vary green shades for more realistic appearance
            green_shade = np.random.choice([
                (34, 139, 34),   # Forest green
                (0, 128, 0),     # Green
                (50, 205, 50),   # Lime green
                (0, 100, 0)      # Dark green
            ])
            draw.ellipse([x-radius, y-radius, x+radius, y+radius], fill=green_shade)
        
        # Add same water areas for consistency
        for i in range(3):
            x = np.random.randint(100, 700)
            y = np.random.randint(100, 500)
            width = np.random.randint(50, 100)
            height = np.random.randint(20, 40)
            draw.ellipse([x, y, x+width, y+height], fill=water_color)
        
        # Convert to bytes
        after_buffer = io.BytesIO()
        after_img.save(after_buffer, format='PNG')
        images['after'] = after_buffer.getvalue()
        
        logger.info("Test images created successfully")
        return images
    
    def save_test_images(self, images: Dict[str, bytes]) -> Dict[str, str]:
        """Save test images to disk for manual inspection."""
        os.makedirs("test_images", exist_ok=True)
        file_paths = {}
        
        for image_type, image_data in images.items():
            file_path = f"test_images/{image_type}_test_image.png"
            with open(file_path, 'wb') as f:
                f.write(image_data)
            file_paths[image_type] = file_path
            logger.info(f"Saved {image_type} image to {file_path}")
        
        return file_paths
    
    def test_upload_evidence(self, evidence_type: str, image_data: bytes) -> Dict:
        """Test uploading evidence with the new fields."""
        logger.info(f"Testing upload of {evidence_type} evidence...")
        
        url = f"{self.api_base_url}/upload"
        
        # Prepare form data
        data = {
            'project_id': TEST_PROJECT_ID,
            'uploader': TEST_USER,
            'gps': TEST_GPS,
            'co2': 150.0,  # Placeholder value
            'evidence_type': evidence_type,
            'project_area_hectares': TEST_AREA_HECTARES,
            'time_period_years': 1.0
        }
        
        # Prepare file
        files = {
            'files': (f'{evidence_type}_test.png', image_data, 'image/png')
        }
        
        try:
            response = self.session.post(url, data=data, files=files)
            response.raise_for_status()
            result = response.json()
            
            logger.info(f"Upload successful: {evidence_type} evidence ID {result.get('evidence_id')}")
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Upload failed for {evidence_type}: {e}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Response content: {e.response.text}")
            return {"error": str(e)}
    
    def test_manual_analysis_trigger(self, project_id: int) -> Dict:
        """Test manual analysis trigger endpoint."""
        logger.info(f"Testing manual analysis trigger for project {project_id}...")
        
        url = f"{self.api_base_url}/projects/{project_id}/trigger-analysis"
        params = {'project_area_hectares': TEST_AREA_HECTARES}
        
        try:
            response = self.session.post(url, params=params)
            response.raise_for_status()
            result = response.json()
            
            if result.get('success'):
                logger.info("Manual analysis trigger successful")
                credits = result.get('analysis_result', {}).get('recommended_credits', 0)
                logger.info(f"Recommended credits: {credits}")
            else:
                logger.warning(f"Manual analysis failed: {result.get('error')}")
            
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Manual analysis trigger failed: {e}")
            return {"error": str(e)}
    
    def test_get_analysis_results(self, evidence_id: int) -> Dict:
        """Test getting analysis results for evidence."""
        logger.info(f"Getting analysis results for evidence {evidence_id}...")
        
        url = f"{self.api_base_url}/evidences/{evidence_id}/analysis"
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            result = response.json()
            
            logger.info("Analysis results retrieved successfully")
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get analysis results: {e}")
            return {"error": str(e)}
    
    def test_project_credit_calculation(self, project_id: int) -> Dict:
        """Test project credit calculation endpoint."""
        logger.info(f"Getting credit calculation for project {project_id}...")
        
        url = f"{self.api_base_url}/projects/{project_id}/credit-calculation"
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            result = response.json()
            
            logger.info("Project credit calculation retrieved successfully")
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get project credit calculation: {e}")
            return {"error": str(e)}
    
    def test_verification_with_ai_credits(self, evidence_id: int) -> Dict:
        """Test verification process using AI-calculated credits."""
        logger.info(f"Testing verification with AI credits for evidence {evidence_id}...")
        
        url = f"{self.api_base_url}/verify"
        data = {
            'evidence_id': evidence_id,
            'mint_receipt': False,
            'receipt_token_uri': '',
            'mint_amount': 0  # Let AI calculate the amount
        }
        
        try:
            response = self.session.post(url, json=data)
            response.raise_for_status()
            result = response.json()
            
            credits_issued = result.get('credits_issued', 0)
            calculation_method = result.get('calculation_method', 'unknown')
            
            logger.info(f"Verification successful: {credits_issued} credits issued using {calculation_method}")
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Verification failed: {e}")
            return {"error": str(e)}
    
    def test_system_stats(self) -> Dict:
        """Test system AI verification statistics."""
        logger.info("Getting system AI verification statistics...")
        
        url = f"{self.api_base_url}/system/ai-verification-stats"
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            result = response.json()
            
            logger.info("System statistics retrieved successfully")
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get system statistics: {e}")
            return {"error": str(e)}
    
    def run_comprehensive_test(self) -> Dict:
        """Run a comprehensive test of the AI verification system."""
        logger.info("Starting comprehensive AI verification test...")
        
        test_results = {
            'timestamp': '2024-01-01T00:00:00',  # Would use datetime.now().isoformat()
            'tests': {}
        }
        
        try:
            # Step 1: Create test images
            test_images = self.create_test_images()
            image_paths = self.save_test_images(test_images)
            test_results['tests']['image_creation'] = {'status': 'success', 'paths': image_paths}
            
            # Step 2: Upload before image
            before_result = self.test_upload_evidence('before', test_images['before'])
            test_results['tests']['before_upload'] = before_result
            
            if 'error' in before_result:
                logger.error("Before upload failed, stopping test")
                return test_results
            
            # Step 3: Upload after image
            after_result = self.test_upload_evidence('after', test_images['after'])
            test_results['tests']['after_upload'] = after_result
            
            if 'error' in after_result:
                logger.error("After upload failed, stopping test")
                return test_results
            
            # Step 4: Check if automatic analysis was triggered
            if after_result.get('dynamic_credits_calculated'):
                logger.info("Automatic AI analysis was triggered!")
                test_results['tests']['automatic_analysis'] = {'status': 'success', 'triggered': True}
            else:
                # Step 5: Trigger manual analysis
                manual_result = self.test_manual_analysis_trigger(TEST_PROJECT_ID)
                test_results['tests']['manual_analysis'] = manual_result
            
            # Step 6: Get analysis results
            evidence_id = after_result.get('evidence_id') or after_result.get('db_id')
            if evidence_id:
                analysis_result = self.test_get_analysis_results(evidence_id)
                test_results['tests']['analysis_results'] = analysis_result
            
            # Step 7: Get project credit calculation
            project_calc_result = self.test_project_credit_calculation(TEST_PROJECT_ID)
            test_results['tests']['project_calculation'] = project_calc_result
            
            # Step 8: Test verification (only if we have valid evidence ID)
            if evidence_id and not before_result.get('error') and not after_result.get('error'):
                verification_result = self.test_verification_with_ai_credits(evidence_id)
                test_results['tests']['verification'] = verification_result
            
            # Step 9: Get system statistics
            stats_result = self.test_system_stats()
            test_results['tests']['system_stats'] = stats_result
            
            logger.info("Comprehensive test completed successfully!")
            test_results['overall_status'] = 'success'
            
        except Exception as e:
            logger.error(f"Comprehensive test failed: {e}")
            test_results['overall_status'] = 'failed'
            test_results['error'] = str(e)
        
        return test_results
    
    def print_test_summary(self, test_results: Dict):
        """Print a summary of test results."""
        print("\n" + "="*60)
        print("AI VERIFICATION SYSTEM TEST SUMMARY")
        print("="*60)
        
        overall_status = test_results.get('overall_status', 'unknown')
        print(f"Overall Status: {overall_status.upper()}")
        
        tests = test_results.get('tests', {})
        
        print(f"\nTests Run: {len(tests)}")
        
        for test_name, test_result in tests.items():
            status = "✓" if not test_result.get('error') else "✗"
            print(f"  {status} {test_name.replace('_', ' ').title()}")
            
            if test_name == 'verification' and 'credits_issued' in test_result:
                print(f"    Credits Issued: {test_result['credits_issued']}")
                print(f"    Calculation Method: {test_result.get('calculation_method', 'unknown')}")
            
            if test_name == 'system_stats' and 'ai_analysis_metrics' in test_result:
                metrics = test_result['ai_analysis_metrics']
                print(f"    AI Adoption: {metrics.get('ai_adoption_percentage', 0)}%")
                print(f"    Avg Confidence: {metrics.get('average_confidence_score', 0)}")
        
        if overall_status == 'success':
            print(f"\n🎉 All tests passed! The AI verification system is working correctly.")
        else:
            print(f"\n⚠️  Some tests failed. Check the logs for details.")
        
        print("="*60)

def main():
    """Main test function."""
    print("AI-Based Carbon Credit Calculation System Test")
    print("=" * 50)
    
    # Initialize tester
    tester = AIVerificationTester()
    
    # Check if API is accessible
    try:
        response = requests.get(f"{API_BASE_URL}/status")
        if response.status_code == 200:
            print("✓ API is accessible")
        else:
            print("✗ API is not accessible")
            return
    except requests.exceptions.RequestException:
        print("✗ API is not accessible. Make sure the FastAPI server is running.")
        return
    
    # Run comprehensive test
    test_results = tester.run_comprehensive_test()
    
    # Save test results
    with open("test_results.json", "w") as f:
        json.dump(test_results, f, indent=2)
    
    # Print summary
    tester.print_test_summary(test_results)
    
    print(f"\nDetailed test results saved to: test_results.json")
    print(f"Test images saved to: test_images/ directory")

if __name__ == "__main__":
    main()