import cv2
import numpy as np
from PIL import Image
import io
import logging

logger = logging.getLogger(__name__)

class GreennessAnalyzer:
    """
    Simple greenness analyzer that compares before and after images
    to calculate a vegetation improvement multiplier (0 to 1.5)
    """
    
    def __init__(self):
        self.min_multiplier = 0.0
        self.max_multiplier = 1.5
        self.neutral_multiplier = 1.0
    
    def calculate_greenness_percentage(self, image_data: bytes) -> float:
        """
        Calculate the percentage of green pixels in an image.
        
        Args:
            image_data: Image bytes
            
        Returns:
            Percentage of green pixels (0-100)
        """
        try:
            # Load image
            image_pil = Image.open(io.BytesIO(image_data))
            image_array = np.array(image_pil.convert('RGB'))
            
            # Resize if too large for performance
            if image_array.shape[0] > 512 or image_array.shape[1] > 512:
                image_pil_resized = image_pil.resize((512, 384), Image.Resampling.LANCZOS)
                image_array = np.array(image_pil_resized.convert('RGB'))
            
            # Convert RGB to HSV for better green detection
            hsv_image = cv2.cvtColor(image_array, cv2.COLOR_RGB2HSV)
            
            # Define green color range in HSV
            # Green hue range: 35-85 (broader range to catch various green shades)
            lower_green1 = np.array([35, 40, 40])   # Lower bound for green
            upper_green1 = np.array([85, 255, 255]) # Upper bound for green
            
            # Also catch darker greens
            lower_green2 = np.array([35, 25, 25])   # Darker green lower bound
            upper_green2 = np.array([85, 255, 200]) # Darker green upper bound
            
            # Create masks for green detection
            mask1 = cv2.inRange(hsv_image, lower_green1, upper_green1)
            mask2 = cv2.inRange(hsv_image, lower_green2, upper_green2)
            
            # Combine masks
            green_mask = cv2.bitwise_or(mask1, mask2)
            
            # Calculate percentage of green pixels
            total_pixels = image_array.shape[0] * image_array.shape[1]
            green_pixels = np.sum(green_mask > 0)
            green_percentage = (green_pixels / total_pixels) * 100
            
            logger.info(f"Image greenness analysis: {green_percentage:.1f}% green pixels")
            return green_percentage
            
        except Exception as e:
            logger.error(f"Error calculating greenness: {str(e)}")
            return 0.0
    
    def calculate_green_progress_multiplier(self, before_image_data: bytes, after_image_data: bytes) -> dict:
        """
        Calculate the Green Progress multiplier by comparing before and after images.
        
        Args:
            before_image_data: Before image bytes
            after_image_data: After image bytes
            
        Returns:
            Dictionary with multiplier and analysis details
        """
        try:
            # Calculate greenness for both images
            before_green = self.calculate_greenness_percentage(before_image_data)
            after_green = self.calculate_greenness_percentage(after_image_data)
            
            # Calculate the improvement
            green_improvement = after_green - before_green
            
            # Calculate multiplier based on improvement
            if green_improvement >= 40:  # Massive improvement
                multiplier = 1.5
                progress_level = "Exceptional"
                confidence = "High"
            elif green_improvement >= 25:  # Significant improvement
                multiplier = 1.3
                progress_level = "Significant"
                confidence = "High"
            elif green_improvement >= 15:  # Good improvement
                multiplier = 1.2
                progress_level = "Good"
                confidence = "High"
            elif green_improvement >= 5:   # Moderate improvement
                multiplier = 1.1
                progress_level = "Moderate"
                confidence = "Medium"
            elif green_improvement >= -5:  # Minimal change
                multiplier = 1.0
                progress_level = "Stable"
                confidence = "Medium"
            elif green_improvement >= -15: # Some loss
                multiplier = 0.8
                progress_level = "Slight Decline"
                confidence = "Medium"
            elif green_improvement >= -25: # Significant loss
                multiplier = 0.5
                progress_level = "Moderate Decline"
                confidence = "Medium"
            else:  # Major loss or no vegetation
                multiplier = 0.2
                progress_level = "Significant Decline"
                confidence = "Medium"
            
            # Special case: if both images have very little green (barren land)
            if before_green < 5 and after_green < 5:
                multiplier = 0.0
                progress_level = "No Vegetation Progress"
                confidence = "High"  # High confidence in detecting no progress
            
            # Ensure multiplier is within bounds
            multiplier = max(self.min_multiplier, min(self.max_multiplier, multiplier))
            
            return {
                'green_progress_multiplier': round(multiplier, 3),
                'green_progress_level': progress_level,
                'confidence_level': confidence,
                'before_green_percentage': round(before_green, 1),
                'after_green_percentage': round(after_green, 1),
                'green_improvement': round(green_improvement, 1),
                'analysis_details': {
                    'before_greenness': f"{before_green:.1f}%",
                    'after_greenness': f"{after_green:.1f}%",
                    'improvement': f"{green_improvement:+.1f}%",
                    'justification': self._get_multiplier_justification(multiplier, green_improvement, progress_level)
                }
            }
            
        except Exception as e:
            logger.error(f"Error calculating green progress multiplier: {str(e)}")
            return {
                'green_progress_multiplier': 1.0,
                'green_progress_level': 'Analysis Failed',
                'confidence_level': 'Medium',
                'before_green_percentage': 0.0,
                'after_green_percentage': 0.0,
                'green_improvement': 0.0,
                'analysis_details': {
                    'error': str(e),
                    'justification': 'Could not analyze images, using neutral multiplier'
                }
            }
    
    def _get_multiplier_justification(self, multiplier: float, improvement: float, level: str) -> str:
        """Get human-readable justification for the multiplier."""
        if multiplier >= 1.4:
            return f"{level} vegetation growth ({improvement:+.1f}%) - Maximum credit boost"
        elif multiplier >= 1.2:
            return f"{level} vegetation growth ({improvement:+.1f}%) - High credit boost"
        elif multiplier >= 1.05:
            return f"{level} vegetation growth ({improvement:+.1f}%) - Moderate credit boost"
        elif multiplier >= 0.95:
            return f"{level} vegetation ({improvement:+.1f}%) - Standard calculation"
        elif multiplier >= 0.5:
            return f"{level} in vegetation ({improvement:+.1f}%) - Reduced credits"
        elif multiplier > 0.1:
            return f"{level} in vegetation ({improvement:+.1f}%) - Minimal credits"
        else:
            return f"{level} - No credits awarded"