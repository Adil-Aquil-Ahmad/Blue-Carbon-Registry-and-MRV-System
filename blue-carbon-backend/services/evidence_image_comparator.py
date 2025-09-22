import cv2
import numpy as np
from typing import Dict, List, Tuple, Optional
import logging
import base64
from io import BytesIO
from PIL import Image
import os

logger = logging.getLogger(__name__)

class EvidenceImageComparator:
    """
    Advanced image comparison service for evidence verification.
    Compares before and after images to highlight vegetation changes and improvements.
    """
    
    def __init__(self):
        self.min_contour_area = 100
        self.vegetation_color_ranges = {
            'green_low': np.array([35, 40, 40]),
            'green_high': np.array([85, 255, 255]),
            'light_green_low': np.array([25, 30, 30]),
            'light_green_high': np.array([95, 255, 255])
        }
    
    def load_image_from_path(self, image_path: str) -> Optional[np.ndarray]:
        """Load image from file path."""
        try:
            if not os.path.exists(image_path):
                logger.error(f"Image file not found: {image_path}")
                return None
            
            image = cv2.imread(image_path)
            if image is None:
                logger.error(f"Failed to load image: {image_path}")
                return None
            
            return image
        except Exception as e:
            logger.error(f"Error loading image {image_path}: {str(e)}")
            return None
    
    def preprocess_image(self, image: np.ndarray, target_size: Tuple[int, int] = (800, 600)) -> np.ndarray:
        """Preprocess image for analysis."""
        try:
            # Resize image
            resized = cv2.resize(image, target_size)
            
            # Apply Gaussian blur to reduce noise
            blurred = cv2.GaussianBlur(resized, (5, 5), 0)
            
            return blurred
        except Exception as e:
            logger.error(f"Error preprocessing image: {str(e)}")
            return image
    
    def detect_vegetation_areas(self, image: np.ndarray) -> Tuple[np.ndarray, float]:
        """Detect vegetation areas in the image using color segmentation."""
        try:
            # Convert to HSV for better color segmentation
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            
            # Create masks for different green ranges
            mask1 = cv2.inRange(hsv, self.vegetation_color_ranges['green_low'], 
                               self.vegetation_color_ranges['green_high'])
            mask2 = cv2.inRange(hsv, self.vegetation_color_ranges['light_green_low'], 
                               self.vegetation_color_ranges['light_green_high'])
            
            # Combine masks
            vegetation_mask = cv2.bitwise_or(mask1, mask2)
            
            # Apply morphological operations to clean up the mask
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            vegetation_mask = cv2.morphologyEx(vegetation_mask, cv2.MORPH_OPEN, kernel)
            vegetation_mask = cv2.morphologyEx(vegetation_mask, cv2.MORPH_CLOSE, kernel)
            
            # Calculate vegetation percentage
            total_pixels = image.shape[0] * image.shape[1]
            vegetation_pixels = cv2.countNonZero(vegetation_mask)
            vegetation_percentage = (vegetation_pixels / total_pixels) * 100
            
            return vegetation_mask, vegetation_percentage
            
        except Exception as e:
            logger.error(f"Error detecting vegetation: {str(e)}")
            return np.zeros((image.shape[0], image.shape[1]), dtype=np.uint8), 0.0
    
    def calculate_ndvi(self, image: np.ndarray) -> Tuple[np.ndarray, float]:
        """Calculate NDVI (Normalized Difference Vegetation Index)."""
        try:
            # Convert to float
            image_float = image.astype(np.float32)
            
            # Extract channels (assuming BGR format)
            blue = image_float[:, :, 0]
            green = image_float[:, :, 1]
            red = image_float[:, :, 2]
            
            # Calculate NIR approximation (using green channel as proxy)
            # In real NDVI, this would be near-infrared
            nir = green
            
            # Calculate NDVI: (NIR - Red) / (NIR + Red)
            ndvi = np.divide(nir - red, nir + red, 
                            out=np.zeros_like(nir), where=(nir + red) != 0)
            
            # Normalize to 0-1 range
            ndvi_normalized = (ndvi + 1) / 2
            
            # Calculate average NDVI
            avg_ndvi = np.mean(ndvi_normalized)
            
            return ndvi_normalized, avg_ndvi
            
        except Exception as e:
            logger.error(f"Error calculating NDVI: {str(e)}")
            return np.zeros((image.shape[0], image.shape[1]), dtype=np.float32), 0.0
    
    def compare_images(self, before_image_path: str, after_image_path: str) -> Dict:
        """
        Compare before and after images to detect vegetation changes.
        Returns detailed analysis with highlighted differences.
        """
        try:
            # Load images
            before_img = self.load_image_from_path(before_image_path)
            after_img = self.load_image_from_path(after_image_path)
            
            if before_img is None or after_img is None:
                return {
                    'success': False,
                    'error': 'Failed to load one or both images'
                }
            
            # Preprocess images
            before_processed = self.preprocess_image(before_img)
            after_processed = self.preprocess_image(after_img)
            
            # Detect vegetation in both images
            before_veg_mask, before_veg_percent = self.detect_vegetation_areas(before_processed)
            after_veg_mask, after_veg_percent = self.detect_vegetation_areas(after_processed)
            
            # Calculate NDVI for both images
            before_ndvi, before_ndvi_avg = self.calculate_ndvi(before_processed)
            after_ndvi, after_ndvi_avg = self.calculate_ndvi(after_processed)
            
            # Calculate improvement percentage
            if before_veg_percent > 0:
                vegetation_improvement = ((after_veg_percent - before_veg_percent) / before_veg_percent) * 100
            else:
                # If no vegetation in before image, calculate based on absolute change
                vegetation_improvement = after_veg_percent * 10  # Scale factor for visualization
            
            # Create difference mask
            diff_mask = cv2.absdiff(after_veg_mask, before_veg_mask)
            
            # Create highlighted comparison images
            highlighted_before = self.create_highlighted_image(before_processed, before_veg_mask, (0, 255, 255))  # Yellow
            highlighted_after = self.create_highlighted_image(after_processed, after_veg_mask, (0, 255, 0))    # Green
            highlighted_diff = self.create_highlighted_image(after_processed, diff_mask, (0, 0, 255))          # Red
            
            # Create side-by-side comparison
            comparison_image = self.create_side_by_side_comparison(
                highlighted_before, highlighted_after, highlighted_diff
            )
            
            # Calculate multiplier based on improvement
            if vegetation_improvement > 0:
                multiplier = 1 + (vegetation_improvement / 100)
            else:
                multiplier = 1.0
            
            # Convert images to base64 for frontend display
            comparison_b64 = self.image_to_base64(comparison_image)
            before_highlighted_b64 = self.image_to_base64(highlighted_before)
            after_highlighted_b64 = self.image_to_base64(highlighted_after)
            
            return {
                'success': True,
                'before_vegetation_percentage': round(before_veg_percent, 2),
                'after_vegetation_percentage': round(after_veg_percent, 2),
                'vegetation_improvement_percentage': round(vegetation_improvement, 2),
                'before_ndvi': round(before_ndvi_avg, 4),
                'after_ndvi': round(after_ndvi_avg, 4),
                'ndvi_improvement': round(after_ndvi_avg - before_ndvi_avg, 4),
                'green_multiplier': round(multiplier, 3),
                'comparison_image_b64': comparison_b64,
                'before_highlighted_b64': before_highlighted_b64,
                'after_highlighted_b64': after_highlighted_b64,
                'analysis_summary': {
                    'vegetation_change': 'Improved' if vegetation_improvement > 0 else 'Declined' if vegetation_improvement < 0 else 'No Change',
                    'change_magnitude': 'Significant' if abs(vegetation_improvement) > 10 else 'Moderate' if abs(vegetation_improvement) > 5 else 'Minor',
                    'recommendation': self.generate_recommendation(vegetation_improvement, multiplier)
                }
            }
            
        except Exception as e:
            logger.error(f"Error comparing images: {str(e)}")
            return {
                'success': False,
                'error': f'Image comparison failed: {str(e)}'
            }
    
    def create_highlighted_image(self, image: np.ndarray, mask: np.ndarray, color: Tuple[int, int, int]) -> np.ndarray:
        """Create image with highlighted areas based on mask."""
        try:
            highlighted = image.copy()
            
            # Create colored overlay
            overlay = np.zeros_like(image)
            overlay[mask > 0] = color
            
            # Blend overlay with original image
            alpha = 0.3
            highlighted = cv2.addWeighted(highlighted, 1 - alpha, overlay, alpha, 0)
            
            # Draw contours for better visibility
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                if cv2.contourArea(contour) > self.min_contour_area:
                    cv2.drawContours(highlighted, [contour], -1, color, 2)
            
            return highlighted
            
        except Exception as e:
            logger.error(f"Error creating highlighted image: {str(e)}")
            return image
    
    def create_side_by_side_comparison(self, before: np.ndarray, after: np.ndarray, diff: np.ndarray) -> np.ndarray:
        """Create side-by-side comparison image."""
        try:
            # Ensure all images have the same height
            height = max(before.shape[0], after.shape[0], diff.shape[0])
            before = cv2.resize(before, (int(before.shape[1] * height / before.shape[0]), height))
            after = cv2.resize(after, (int(after.shape[1] * height / after.shape[0]), height))
            diff = cv2.resize(diff, (int(diff.shape[1] * height / diff.shape[0]), height))
            
            # Add labels
            labeled_before = self.add_label_to_image(before, "BEFORE")
            labeled_after = self.add_label_to_image(after, "AFTER")
            labeled_diff = self.add_label_to_image(diff, "CHANGES")
            
            # Concatenate horizontally
            comparison = np.hstack([labeled_before, labeled_after, labeled_diff])
            
            return comparison
            
        except Exception as e:
            logger.error(f"Error creating comparison: {str(e)}")
            return before
    
    def add_label_to_image(self, image: np.ndarray, label: str) -> np.ndarray:
        """Add text label to image."""
        try:
            labeled = image.copy()
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.8
            color = (255, 255, 255)
            thickness = 2
            
            # Get text size
            (text_width, text_height), _ = cv2.getTextSize(label, font, font_scale, thickness)
            
            # Create background rectangle
            cv2.rectangle(labeled, (10, 10), (text_width + 20, text_height + 20), (0, 0, 0), -1)
            
            # Add text
            cv2.putText(labeled, label, (15, text_height + 15), font, font_scale, color, thickness)
            
            return labeled
            
        except Exception as e:
            logger.error(f"Error adding label: {str(e)}")
            return image
    
    def image_to_base64(self, image: np.ndarray) -> str:
        """Convert OpenCV image to base64 string."""
        try:
            # Convert BGR to RGB
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Convert to PIL Image
            pil_image = Image.fromarray(image_rgb)
            
            # Save to buffer
            buffer = BytesIO()
            pil_image.save(buffer, format='PNG')
            
            # Encode to base64
            img_str = base64.b64encode(buffer.getvalue()).decode()
            
            return f"data:image/png;base64,{img_str}"
            
        except Exception as e:
            logger.error(f"Error converting image to base64: {str(e)}")
            return ""
    
    def generate_recommendation(self, improvement: float, multiplier: float) -> str:
        """Generate recommendation based on analysis results."""
        if improvement > 20:
            return "Excellent vegetation improvement! Strong evidence of successful restoration."
        elif improvement > 10:
            return "Good vegetation growth detected. Project showing positive progress."
        elif improvement > 0:
            return "Modest vegetation improvement observed. Monitor for continued growth."
        elif improvement == 0:
            return "No significant vegetation change detected. May need additional monitoring period."
        else:
            return "Vegetation decline detected. Investigation recommended to identify causes."
    
    def get_evidence_images_analysis(self, evidence_id: int) -> Dict:
        """
        Get detailed analysis for evidence images including highlighted comparisons.
        This is the main method to be called from the API.
        """
        try:
            # This would typically fetch from database to get actual file paths
            # For now, using file path pattern and scanning uploads directory
            uploads_dir = "uploads"
            
            # Look for before and after images for this evidence
            before_path = None
            after_path = None
            evidence_files = []
            
            # Scan uploads directory for evidence files
            if os.path.exists(uploads_dir):
                for filename in os.listdir(uploads_dir):
                    # Look for files that might belong to this evidence
                    if (str(evidence_id) in filename or 
                        filename.startswith(f"evidence_{evidence_id}") or
                        filename.endswith(f"_{evidence_id}.jpg") or
                        filename.endswith(f"_{evidence_id}.jpeg") or
                        filename.endswith(f"_{evidence_id}.png")):
                        
                        full_path = os.path.join(uploads_dir, filename)
                        evidence_files.append((filename, full_path))
                        
                        # Try to determine before/after based on filename
                        filename_lower = filename.lower()
                        if "before" in filename_lower:
                            before_path = full_path
                        elif "after" in filename_lower:
                            after_path = full_path
                        elif before_path is None:
                            before_path = full_path
                        elif after_path is None:
                            after_path = full_path
            
            # If we didn't find files by evidence ID pattern, look for recent files
            if not evidence_files and os.path.exists(uploads_dir):
                all_files = []
                for filename in os.listdir(uploads_dir):
                    if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                        full_path = os.path.join(uploads_dir, filename)
                        stat = os.stat(full_path)
                        all_files.append((filename, full_path, stat.st_mtime))
                
                # Sort by modification time and take the 2 most recent
                all_files.sort(key=lambda x: x[2], reverse=True)
                
                if len(all_files) >= 2:
                    before_path = all_files[1][1]  # Second most recent
                    after_path = all_files[0][1]   # Most recent
                    evidence_files = [(all_files[1][0], before_path), (all_files[0][0], after_path)]
            
            if not before_path or not after_path:
                return {
                    'success': False,
                    'error': f'Could not find both before and after images for evidence {evidence_id}. Found files: {[f[0] for f in evidence_files]}',
                    'available_files': [f[0] for f in evidence_files]
                }
            
            logger.info(f"Using images for evidence {evidence_id}: before={os.path.basename(before_path)}, after={os.path.basename(after_path)}")
            
            # Perform comparison
            result = self.compare_images(before_path, after_path)
            
            # Add file information to result
            if result.get('success'):
                result['files_used'] = {
                    'before_image': os.path.basename(before_path),
                    'after_image': os.path.basename(after_path),
                    'evidence_id': evidence_id
                }
            
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing evidence {evidence_id}: {str(e)}")
            return {
                'success': False,
                'error': f'Analysis failed: {str(e)}'
            }