import cv2
import numpy as np
from PIL import Image, ImageEnhance
import io
import base64
from typing import Dict, List, Tuple, Optional
import json
from datetime import datetime
import logging
from .co2_sequestration_calculator import CO2SequestrationCalculator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NDVIAnalyzer:
    """
    Advanced NDVI (Normalized Difference Vegetation Index) analyzer for blue carbon vegetation detection.
    
    NDVI = (NIR - Red) / (NIR + Red)
    Where NIR = Near Infrared and Red = Red band reflectance
    
    For RGB images, we approximate NIR using green channel and red channel analysis.
    """
    
    def __init__(self):
        self.min_vegetation_threshold = 0.2  # Minimum NDVI for vegetation detection
        self.healthy_vegetation_threshold = 0.4  # NDVI threshold for healthy vegetation
        self.mangrove_specific_threshold = 0.5  # Higher threshold for mangrove identification
        
    def calculate_ndvi_rgb(self, image: np.ndarray) -> np.ndarray:
        """
        Calculate NDVI from RGB image using approximation method.
        For RGB images, we use Green as NIR proxy and Red channel.
        """
        try:
            # Convert to float to prevent overflow
            image_float = image.astype(np.float64)
            
            # Extract channels (RGB format)
            red_channel = image_float[:, :, 0]
            green_channel = image_float[:, :, 1]  # Use green as NIR proxy
            blue_channel = image_float[:, :, 2]
            
            # Calculate modified NDVI using green as NIR approximation
            # This is a simplified approach for RGB images
            nir_proxy = green_channel + (blue_channel * 0.3)  # Enhanced NIR proxy
            red = red_channel
            
            # Avoid division by zero
            denominator = nir_proxy + red
            denominator = np.where(denominator == 0, 1, denominator)
            
            # Calculate NDVI
            ndvi = (nir_proxy - red) / denominator
            
            # Normalize to -1 to 1 range
            ndvi = np.clip(ndvi, -1, 1)
            
            return ndvi
            
        except Exception as e:
            logger.error(f"Error calculating NDVI: {str(e)}")
            return np.zeros_like(image[:, :, 0])
    
    def enhanced_vegetation_detection(self, image: np.ndarray) -> Dict:
        """
        Enhanced vegetation detection using multiple color space analysis.
        """
        try:
            # Convert to different color spaces for better analysis
            hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
            lab = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
            
            # HSV-based vegetation detection (green hue analysis)
            hue = hsv[:, :, 0]
            saturation = hsv[:, :, 1]
            value = hsv[:, :, 2]
            
            # Define green range in HSV (adjusted for vegetation)
            green_mask_lower = (35 <= hue) & (hue <= 85)  # Green hue range
            green_mask_saturation = saturation > 30  # Minimum saturation
            green_mask_value = value > 20  # Minimum brightness
            
            vegetation_mask_hsv = green_mask_lower & green_mask_saturation & green_mask_value
            
            # LAB color space analysis for better vegetation detection
            a_channel = lab[:, :, 1]  # Green-Red component
            b_channel = lab[:, :, 2]  # Blue-Yellow component
            
            # Vegetation typically has negative 'a' values (more green than red)
            vegetation_mask_lab = a_channel < 127  # Below neutral (more green)
            
            # Combine masks
            combined_vegetation_mask = vegetation_mask_hsv | vegetation_mask_lab
            
            # Calculate vegetation statistics
            total_pixels = image.shape[0] * image.shape[1]
            vegetation_pixels = np.sum(combined_vegetation_mask)
            vegetation_percentage = (vegetation_pixels / total_pixels) * 100
            
            return {
                'vegetation_mask': combined_vegetation_mask,
                'vegetation_percentage': vegetation_percentage,
                'total_pixels': total_pixels,
                'vegetation_pixels': vegetation_pixels
            }
            
        except Exception as e:
            logger.error(f"Error in enhanced vegetation detection: {str(e)}")
            return {
                'vegetation_mask': np.zeros((image.shape[0], image.shape[1]), dtype=bool),
                'vegetation_percentage': 0.0,
                'total_pixels': image.shape[0] * image.shape[1],
                'vegetation_pixels': 0
            }
    
    def analyze_image_composition(self, image: np.ndarray) -> Dict:
        """
        Analyze image composition to detect planted vs empty areas.
        """
        try:
            # Convert to grayscale for texture analysis
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            
            # Calculate texture features using standard deviation
            kernel_size = 9
            texture = cv2.Laplacian(gray, cv2.CV_64F, ksize=kernel_size)
            texture_std = np.std(texture)
            
            # Color variance analysis
            color_variance = np.var(image, axis=(0, 1))
            avg_color_variance = np.mean(color_variance)
            
            # Detect bare soil/sand areas (typically brown/tan colors)
            hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
            hue = hsv[:, :, 0]
            saturation = hsv[:, :, 1]
            
            # Brown/tan soil detection
            soil_mask = ((10 <= hue) & (hue <= 30)) & (saturation > 20)
            soil_percentage = (np.sum(soil_mask) / (image.shape[0] * image.shape[1])) * 100
            
            # Water detection (blue areas)
            water_mask = ((100 <= hue) & (hue <= 130)) & (saturation > 30)
            water_percentage = (np.sum(water_mask) / (image.shape[0] * image.shape[1])) * 100
            
            return {
                'texture_complexity': texture_std,
                'color_variance': avg_color_variance,
                'soil_percentage': soil_percentage,
                'water_percentage': water_percentage,
                'soil_mask': soil_mask,
                'water_mask': water_mask
            }
            
        except Exception as e:
            logger.error(f"Error analyzing image composition: {str(e)}")
            return {
                'texture_complexity': 0.0,
                'color_variance': 0.0,
                'soil_percentage': 0.0,
                'water_percentage': 0.0,
                'soil_mask': np.zeros((image.shape[0], image.shape[1]), dtype=bool),
                'water_mask': np.zeros((image.shape[0], image.shape[1]), dtype=bool)
            }
    
    def calculate_health_metrics(self, ndvi: np.ndarray, vegetation_data: Dict) -> Dict:
        """
        Calculate vegetation health metrics from NDVI and other data.
        """
        try:
            # NDVI statistics
            ndvi_mean = np.mean(ndvi)
            ndvi_std = np.std(ndvi)
            ndvi_max = np.max(ndvi)
            ndvi_min = np.min(ndvi)
            
            # Health classification based on NDVI values
            healthy_vegetation = ndvi > self.healthy_vegetation_threshold
            moderate_vegetation = (ndvi > self.min_vegetation_threshold) & (ndvi <= self.healthy_vegetation_threshold)
            sparse_vegetation = (ndvi > 0) & (ndvi <= self.min_vegetation_threshold)
            no_vegetation = ndvi <= 0
            
            total_pixels = ndvi.size
            healthy_percentage = (np.sum(healthy_vegetation) / total_pixels) * 100
            moderate_percentage = (np.sum(moderate_vegetation) / total_pixels) * 100
            sparse_percentage = (np.sum(sparse_vegetation) / total_pixels) * 100
            bare_percentage = (np.sum(no_vegetation) / total_pixels) * 100
            
            # Overall health index (weighted score)
            health_index = (
                (healthy_percentage * 1.0) +
                (moderate_percentage * 0.7) +
                (sparse_percentage * 0.3) +
                (bare_percentage * 0.0)
            )
            
            # Mangrove-specific detection
            potential_mangrove_pixels = ndvi > self.mangrove_specific_threshold
            mangrove_likelihood = (np.sum(potential_mangrove_pixels) / total_pixels) * 100
            
            return {
                'ndvi_mean': float(ndvi_mean),
                'ndvi_std': float(ndvi_std),
                'ndvi_max': float(ndvi_max),
                'ndvi_min': float(ndvi_min),
                'healthy_percentage': float(healthy_percentage),
                'moderate_percentage': float(moderate_percentage),
                'sparse_percentage': float(sparse_percentage),
                'bare_percentage': float(bare_percentage),
                'health_index': float(health_index),
                'mangrove_likelihood': float(mangrove_likelihood),
                'is_mangrove_detected': mangrove_likelihood > 15.0  # Threshold for mangrove detection
            }
            
        except Exception as e:
            logger.error(f"Error calculating health metrics: {str(e)}")
            return {
                'ndvi_mean': 0.0,
                'ndvi_std': 0.0,
                'ndvi_max': 0.0,
                'ndvi_min': 0.0,
                'healthy_percentage': 0.0,
                'moderate_percentage': 0.0,
                'sparse_percentage': 0.0,
                'bare_percentage': 100.0,
                'health_index': 0.0,
                'mangrove_likelihood': 0.0,
                'is_mangrove_detected': False
            }
    
    def analyze_image(self, image_data: bytes, filename: str = "unknown") -> Dict:
        """
        Main analysis function that processes an image and returns comprehensive results.
        """
        try:
            # Load image
            image_pil = Image.open(io.BytesIO(image_data))
            image_array = np.array(image_pil.convert('RGB'))
            
            logger.info(f"Analyzing image: {filename}, Shape: {image_array.shape}")
            
            # Resize if too large (for performance)
            if image_array.shape[0] > 1024 or image_array.shape[1] > 1024:
                image_pil_resized = image_pil.resize((1024, 768), Image.Resampling.LANCZOS)
                image_array = np.array(image_pil_resized.convert('RGB'))
            
            # Calculate NDVI
            ndvi = self.calculate_ndvi_rgb(image_array)
            
            # Enhanced vegetation detection
            vegetation_data = self.enhanced_vegetation_detection(image_array)
            
            # Image composition analysis
            composition_data = self.analyze_image_composition(image_array)
            
            # Health metrics
            health_metrics = self.calculate_health_metrics(ndvi, vegetation_data)
            
            # Calculate confidence score
            confidence_factors = [
                min(vegetation_data['vegetation_percentage'] / 50.0, 1.0),  # Vegetation coverage
                min(health_metrics['health_index'] / 80.0, 1.0),          # Health index
                min(composition_data['texture_complexity'] / 100.0, 1.0),  # Texture complexity
                1.0 - min(composition_data['water_percentage'] / 100.0, 0.5)  # Water reduction factor
            ]
            
            confidence_score = (sum(confidence_factors) / len(confidence_factors)) * 100
            confidence_score = max(min(confidence_score, 95.0), 60.0)  # Clamp between 60-95%
            
            # Generate summary
            analysis_summary = self.generate_analysis_summary(
                health_metrics, vegetation_data, composition_data, confidence_score
            )
            
            # Prepare result
            result = {
                'filename': filename,
                'timestamp': datetime.now().isoformat(),
                'image_dimensions': {
                    'width': image_array.shape[1],
                    'height': image_array.shape[0],
                    'channels': image_array.shape[2]
                },
                'ndvi_analysis': {
                    'mean_ndvi': health_metrics['ndvi_mean'],
                    'max_ndvi': health_metrics['ndvi_max'],
                    'min_ndvi': health_metrics['ndvi_min'],
                    'std_ndvi': health_metrics['ndvi_std']
                },
                'vegetation_analysis': {
                    'total_vegetation_coverage': vegetation_data['vegetation_percentage'],
                    'healthy_vegetation': health_metrics['healthy_percentage'],
                    'moderate_vegetation': health_metrics['moderate_percentage'],
                    'sparse_vegetation': health_metrics['sparse_percentage'],
                    'bare_land': health_metrics['bare_percentage']
                },
                'composition_analysis': {
                    'soil_percentage': composition_data['soil_percentage'],
                    'water_percentage': composition_data['water_percentage'],
                    'texture_complexity': composition_data['texture_complexity'],
                    'color_variance': composition_data['color_variance']
                },
                'detection_results': {
                    'mangrove_detected': health_metrics['is_mangrove_detected'],
                    'mangrove_likelihood': health_metrics['mangrove_likelihood'],
                    'overall_health_index': health_metrics['health_index']
                },
                'verification_metrics': {
                    'confidence_score': confidence_score,
                    'planted_area_estimate': max(0, vegetation_data['vegetation_percentage'] - composition_data['water_percentage']),
                    'empty_land_estimate': composition_data['soil_percentage'] + health_metrics['bare_percentage'] / 2,
                    'analysis_quality': 'High' if confidence_score > 85 else 'Medium' if confidence_score > 70 else 'Basic'
                },
                'summary': analysis_summary
            }
            
            logger.info(f"Analysis completed for {filename}. Confidence: {confidence_score:.1f}%")
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing image {filename}: {str(e)}")
            return {
                'filename': filename,
                'timestamp': datetime.now().isoformat(),
                'error': str(e),
                'success': False
            }
    
    def generate_analysis_summary(self, health_metrics: Dict, vegetation_data: Dict, 
                                composition_data: Dict, confidence_score: float) -> str:
        """
        Generate a human-readable summary of the analysis results.
        """
        try:
            summary_parts = []
            
            # Vegetation coverage assessment
            veg_coverage = vegetation_data['vegetation_percentage']
            if veg_coverage > 60:
                summary_parts.append("High vegetation coverage detected")
            elif veg_coverage > 30:
                summary_parts.append("Moderate vegetation coverage observed")
            elif veg_coverage > 10:
                summary_parts.append("Limited vegetation coverage identified")
            else:
                summary_parts.append("Minimal vegetation detected")
            
            # Mangrove detection
            if health_metrics['is_mangrove_detected']:
                summary_parts.append("mangrove-like vegetation patterns identified")
            
            # Health assessment
            health_index = health_metrics['health_index']
            if health_index > 70:
                summary_parts.append("vegetation appears healthy")
            elif health_index > 40:
                summary_parts.append("vegetation shows moderate health")
            else:
                summary_parts.append("vegetation health needs attention")
            
            # Land composition
            if composition_data['soil_percentage'] > 30:
                summary_parts.append("significant exposed soil areas present")
            if composition_data['water_percentage'] > 20:
                summary_parts.append("water bodies identified in analysis area")
            
            # Confidence qualifier
            if confidence_score > 85:
                confidence_qualifier = "High confidence in analysis results."
            elif confidence_score > 70:
                confidence_qualifier = "Good confidence in analysis results."
            else:
                confidence_qualifier = "Basic analysis - consider additional verification."
            
            summary = ". ".join(summary_parts).capitalize() + f". {confidence_qualifier}"
            return summary
            
        except Exception as e:
            logger.error(f"Error generating summary: {str(e)}")
            return "Analysis completed with basic vegetation detection results."


class BeforeAfterAnalyzer:
    """
    Specialized analyzer for comparing before and after images to assess
    land transformation and carbon sequestration potential.
    """
    
    def __init__(self):
        self.ndvi_analyzer = NDVIAnalyzer()
        self.co2_calculator = CO2SequestrationCalculator()
    
    def compare_images(self, before_image_data: bytes, after_image_data: bytes, 
                      project_area_hectares: float, time_period_years: float = 1.0) -> Dict:
        """
        Compare before and after images to assess transformation and calculate carbon credits.
        """
        try:
            logger.info("Starting before/after image comparison analysis")
            
            # Analyze both images
            before_analysis = self.ndvi_analyzer.analyze_image(before_image_data, "before_image")
            after_analysis = self.ndvi_analyzer.analyze_image(after_image_data, "after_image")
            
            if 'error' in before_analysis or 'error' in after_analysis:
                return {
                    'error': 'Failed to analyze one or both images',
                    'before_analysis_success': 'error' not in before_analysis,
                    'after_analysis_success': 'error' not in after_analysis
                }
            
            # Calculate transformation metrics
            transformation_metrics = self._calculate_detailed_transformation(before_analysis, after_analysis)
            
            # Calculate CO2 sequestration
            co2_results = self.co2_calculator.calculate_co2_sequestration(
                before_analysis, after_analysis, project_area_hectares, time_period_years
            )
            
            # Calculate carbon credits
            credit_results = self.co2_calculator.calculate_carbon_credits(
                co2_results['co2_sequestration_kg']
            )
            
            # Generate comprehensive analysis report
            analysis_report = self._generate_comparison_report(
                before_analysis, after_analysis, transformation_metrics, co2_results, credit_results
            )
            
            # Calculate overall verification score
            verification_score = self._calculate_verification_score(
                transformation_metrics, co2_results, before_analysis, after_analysis
            )
            
            result = {
                'timestamp': datetime.now().isoformat(),
                'analysis_type': 'before_after_comparison',
                'project_area_hectares': project_area_hectares,
                'time_period_years': time_period_years,
                
                # Individual image analyses
                'before_analysis': before_analysis,
                'after_analysis': after_analysis,
                
                # Transformation analysis
                'transformation_metrics': transformation_metrics,
                
                # CO2 and carbon credit calculations
                'co2_sequestration': co2_results,
                'carbon_credits': credit_results,
                
                # Verification metrics
                'verification_score': verification_score,
                'recommended_credits': credit_results['carbon_credits'],
                
                # Comprehensive report
                'analysis_report': analysis_report,
                'success': True
            }
            
            logger.info(f"Before/after analysis completed. Recommended credits: {credit_results['carbon_credits']}")
            return result
            
        except Exception as e:
            logger.error(f"Error in before/after image comparison: {str(e)}")
            return {
                'error': str(e),
                'success': False,
                'timestamp': datetime.now().isoformat()
            }
    
    def _calculate_detailed_transformation(self, before_analysis: Dict, after_analysis: Dict) -> Dict:
        """
        Calculate detailed transformation metrics between before and after images.
        """
        try:
            # Basic transformation metrics from CO2 calculator
            basic_transformation = self.co2_calculator.calculate_vegetation_transformation(
                before_analysis, after_analysis
            )
            
            # Additional detailed metrics
            before_veg = before_analysis['vegetation_analysis']
            after_veg = after_analysis['vegetation_analysis']
            before_ndvi = before_analysis['ndvi_analysis']
            after_ndvi = after_analysis['ndvi_analysis']
            before_comp = before_analysis['composition_analysis']
            after_comp = after_analysis['composition_analysis']
            
            # Detailed vegetation changes
            vegetation_details = {
                'healthy_vegetation_change': after_veg['healthy_vegetation'] - before_veg['healthy_vegetation'],
                'moderate_vegetation_change': after_veg['moderate_vegetation'] - before_veg['moderate_vegetation'],
                'sparse_vegetation_change': after_veg['sparse_vegetation'] - before_veg['sparse_vegetation'],
                'bare_land_change': after_veg['bare_land'] - before_veg['bare_land']
            }
            
            # NDVI analysis
            ndvi_details = {
                'mean_ndvi_change': after_ndvi['mean_ndvi'] - before_ndvi['mean_ndvi'],
                'max_ndvi_change': after_ndvi['max_ndvi'] - before_ndvi['max_ndvi'],
                'ndvi_std_change': after_ndvi['std_ndvi'] - before_ndvi['std_ndvi']
            }
            
            # Composition changes
            composition_details = {
                'soil_percentage_change': after_comp['soil_percentage'] - before_comp['soil_percentage'],
                'water_percentage_change': after_comp['water_percentage'] - before_comp['water_percentage'],
                'texture_complexity_change': after_comp['texture_complexity'] - before_comp['texture_complexity']
            }
            
            # Land use change classification
            land_use_change = self._classify_land_use_change(
                before_veg, after_veg, before_comp, after_comp
            )
            
            # Combine all metrics
            detailed_transformation = {
                **basic_transformation,
                'vegetation_details': vegetation_details,
                'ndvi_details': ndvi_details,
                'composition_details': composition_details,
                'land_use_change': land_use_change,
                'transformation_quality': self._assess_transformation_quality(basic_transformation),
                'ecosystem_improvement_score': self._calculate_ecosystem_improvement_score(
                    vegetation_details, ndvi_details, composition_details
                )
            }
            
            return detailed_transformation
            
        except Exception as e:
            logger.error(f"Error calculating detailed transformation: {e}")
            return {}
    
    def _classify_land_use_change(self, before_veg: Dict, after_veg: Dict, 
                                 before_comp: Dict, after_comp: Dict) -> Dict:
        """
        Classify the type of land use change based on comprehensive analysis.
        """
        try:
            # Determine dominant land cover before and after
            before_dominant = self._get_dominant_land_cover(before_veg, before_comp)
            after_dominant = self._get_dominant_land_cover(after_veg, after_comp)
            
            # Calculate change intensity
            veg_change = after_veg['total_vegetation_coverage'] - before_veg['total_vegetation_coverage']
            change_intensity = 'high' if abs(veg_change) > 30 else 'medium' if abs(veg_change) > 15 else 'low'
            
            # Determine change direction
            change_direction = 'improvement' if veg_change > 5 else 'degradation' if veg_change < -5 else 'stable'
            
            return {
                'before_dominant_cover': before_dominant,
                'after_dominant_cover': after_dominant,
                'change_type': f"{before_dominant}_to_{after_dominant}",
                'change_direction': change_direction,
                'change_intensity': change_intensity,
                'vegetation_change_magnitude': abs(veg_change),
                'is_restoration_project': (before_dominant in ['bare_land', 'degraded'] and 
                                         after_dominant in ['dense_vegetation', 'moderate_vegetation'])
            }
            
        except Exception as e:
            logger.error(f"Error classifying land use change: {e}")
            return {}
    
    def _get_dominant_land_cover(self, vegetation: Dict, composition: Dict) -> str:
        """
        Determine the dominant land cover type from analysis results.
        """
        total_veg = vegetation.get('total_vegetation_coverage', 0)
        bare_land = vegetation.get('bare_land', 0)
        water = composition.get('water_percentage', 0)
        soil = composition.get('soil_percentage', 0)
        
        if water > 40:
            return 'water_dominated'
        elif total_veg > 60:
            return 'dense_vegetation'
        elif total_veg > 30:
            return 'moderate_vegetation'
        elif total_veg > 10:
            return 'sparse_vegetation'
        elif soil > 40 or bare_land > 50:
            return 'bare_land'
        else:
            return 'degraded'
    
    def _assess_transformation_quality(self, transformation: Dict) -> str:
        """
        Assess the quality of transformation based on multiple factors.
        """
        try:
            score = transformation.get('transformation_score', 0)
            veg_change = transformation.get('vegetation_change_percentage', 0)
            ndvi_improvement = transformation.get('ndvi_improvement', 0)
            
            if score > 80 and veg_change > 25 and ndvi_improvement > 0.3:
                return 'excellent'
            elif score > 60 and veg_change > 15 and ndvi_improvement > 0.2:
                return 'very_good'
            elif score > 40 and veg_change > 10 and ndvi_improvement > 0.1:
                return 'good'
            elif score > 20 and veg_change > 5:
                return 'moderate'
            elif veg_change > 0:
                return 'minimal'
            else:
                return 'poor'
                
        except Exception:
            return 'unknown'
    
    def _calculate_ecosystem_improvement_score(self, veg_details: Dict, 
                                             ndvi_details: Dict, comp_details: Dict) -> float:
        """
        Calculate a comprehensive ecosystem improvement score (0-100).
        """
        try:
            # Vegetation improvement component (0-40 points)
            veg_score = (
                max(veg_details.get('healthy_vegetation_change', 0), 0) * 1.5 +
                max(veg_details.get('moderate_vegetation_change', 0), 0) * 1.0 +
                max(-veg_details.get('bare_land_change', 0), 0) * 0.5
            )
            veg_score = min(veg_score, 40)
            
            # NDVI improvement component (0-30 points)
            ndvi_score = max(ndvi_details.get('mean_ndvi_change', 0), 0) * 100
            ndvi_score = min(ndvi_score, 30)
            
            # Composition improvement component (0-30 points)
            comp_score = (
                max(-comp_details.get('soil_percentage_change', 0), 0) * 0.5 +
                max(comp_details.get('texture_complexity_change', 0), 0) * 0.1
            )
            comp_score = min(comp_score, 30)
            
            total_score = veg_score + ndvi_score + comp_score
            return min(max(total_score, 0), 100)
            
        except Exception as e:
            logger.error(f"Error calculating ecosystem improvement score: {e}")
            return 0
    
    def _calculate_verification_score(self, transformation: Dict, co2_results: Dict,
                                    before_analysis: Dict, after_analysis: Dict) -> Dict:
        """
        Calculate overall verification score and confidence metrics.
        """
        try:
            # Base confidence from image analysis
            before_confidence = before_analysis.get('verification_metrics', {}).get('confidence_score', 70)
            after_confidence = after_analysis.get('verification_metrics', {}).get('confidence_score', 70)
            image_confidence = (before_confidence + after_confidence) / 2
            
            # Transformation confidence
            transformation_score = transformation.get('transformation_score', 0)
            transformation_quality = transformation.get('transformation_quality', 'poor')
            quality_multiplier = {
                'excellent': 1.0, 'very_good': 0.9, 'good': 0.8, 
                'moderate': 0.7, 'minimal': 0.6, 'poor': 0.4
            }.get(transformation_quality, 0.5)
            
            # CO2 calculation confidence
            co2_confidence = co2_results.get('confidence_factor', 0.8) * 100
            
            # Overall verification score
            overall_score = (
                image_confidence * 0.4 +
                transformation_score * quality_multiplier * 0.4 +
                co2_confidence * 0.2
            )
            
            return {
                'overall_verification_score': round(overall_score, 1),
                'image_analysis_confidence': round(image_confidence, 1),
                'transformation_confidence': round(transformation_score * quality_multiplier, 1),
                'co2_calculation_confidence': round(co2_confidence, 1),
                'transformation_quality': transformation_quality,
                'verification_level': self._get_verification_level(overall_score),
                'recommended_action': self._get_recommended_action(overall_score, transformation_quality)
            }
            
        except Exception as e:
            logger.error(f"Error calculating verification score: {e}")
            return {
                'overall_verification_score': 0,
                'verification_level': 'insufficient',
                'recommended_action': 'require_manual_review'
            }
    
    def _get_verification_level(self, score: float) -> str:
        """Get verification level based on overall score."""
        if score >= 85:
            return 'high_confidence'
        elif score >= 70:
            return 'good_confidence'
        elif score >= 55:
            return 'moderate_confidence'
        elif score >= 40:
            return 'low_confidence'
        else:
            return 'insufficient'
    
    def _get_recommended_action(self, score: float, quality: str) -> str:
        """Get recommended action based on verification metrics."""
        if score >= 80 and quality in ['excellent', 'very_good']:
            return 'approve_full_credits'
        elif score >= 65 and quality in ['good', 'very_good']:
            return 'approve_with_monitoring'
        elif score >= 50:
            return 'approve_partial_credits'
        elif score >= 35:
            return 'require_additional_evidence'
        else:
            return 'require_manual_review'
    
    def _generate_comparison_report(self, before_analysis: Dict, after_analysis: Dict,
                                  transformation: Dict, co2_results: Dict, 
                                  credit_results: Dict) -> str:
        """
        Generate a comprehensive human-readable analysis report.
        """
        try:
            report_parts = []
            
            # Executive Summary
            veg_change = transformation.get('vegetation_change_percentage', 0)
            co2_kg = co2_results.get('co2_sequestration_kg', 0)
            credits = credit_results.get('carbon_credits', 0)
            quality = transformation.get('transformation_quality', 'unknown')
            
            report_parts.append(f"EXECUTIVE SUMMARY:")
            report_parts.append(f"Vegetation coverage changed by {veg_change:.1f}%, resulting in {co2_kg:.1f} kg CO₂ sequestration")
            report_parts.append(f"Transformation quality: {quality.title()}")
            report_parts.append(f"Recommended carbon credits: {credits:.2f}")
            report_parts.append("")
            
            # Detailed Analysis
            report_parts.append("DETAILED ANALYSIS:")
            
            # Before state
            before_veg = before_analysis.get('vegetation_analysis', {}).get('total_vegetation_coverage', 0)
            after_veg = after_analysis.get('vegetation_analysis', {}).get('total_vegetation_coverage', 0)
            report_parts.append(f"• Before: {before_veg:.1f}% vegetation coverage")
            report_parts.append(f"• After: {after_veg:.1f}% vegetation coverage")
            report_parts.append(f"• Net change: {after_veg - before_veg:.1f} percentage points")
            
            # NDVI changes
            before_ndvi = before_analysis.get('ndvi_analysis', {}).get('mean_ndvi', 0)
            after_ndvi = after_analysis.get('ndvi_analysis', {}).get('mean_ndvi', 0)
            report_parts.append(f"• NDVI improvement: {after_ndvi - before_ndvi:.3f}")
            
            # Ecosystem type and transformation
            ecosystem = co2_results.get('ecosystem_type', 'unknown')
            transformation_type = transformation.get('transformation_type', 'unknown')
            report_parts.append(f"• Detected ecosystem: {ecosystem.replace('_', ' ').title()}")
            report_parts.append(f"• Transformation type: {transformation_type.replace('_', ' ').title()}")
            
            # Carbon calculation details
            report_parts.append("")
            report_parts.append("CARBON SEQUESTRATION CALCULATION:")
            base_rate = co2_results.get('base_rate_kg_ha_year', 0)
            area = co2_results.get('project_area_hectares', 0)
            report_parts.append(f"• Base sequestration rate: {base_rate:.1f} kg CO₂/ha/year")
            report_parts.append(f"• Project area: {area:.2f} hectares")
            report_parts.append(f"• Transformation multiplier: {co2_results.get('transformation_multiplier', 1):.2f}")
            report_parts.append(f"• NDVI multiplier: {co2_results.get('ndvi_multiplier', 1):.2f}")
            report_parts.append(f"• Total CO₂ sequestration: {co2_kg:.1f} kg ({co2_results.get('co2_sequestration_tonnes', 0):.3f} tonnes)")
            
            return "\n".join(report_parts)
            
        except Exception as e:
            logger.error(f"Error generating comparison report: {e}")
            return "Error generating analysis report. Please review individual analysis components."


class VideoAnalyzer:
    """
    Video analysis for temporal vegetation monitoring.
    """
    
    def __init__(self):
        self.ndvi_analyzer = NDVIAnalyzer()
        self.frame_interval = 30  # Analyze every 30th frame
    
    def extract_key_frames(self, video_path: str, max_frames: int = 10) -> List[np.ndarray]:
        """
        Extract key frames from video for analysis.
        """
        try:
            cap = cv2.VideoCapture(video_path)
            frames = []
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            # Calculate frame interval
            if frame_count > max_frames:
                interval = frame_count // max_frames
            else:
                interval = 1
            
            frame_number = 0
            while cap.isOpened() and len(frames) < max_frames:
                ret, frame = cap.read()
                if not ret:
                    break
                
                if frame_number % interval == 0:
                    # Convert BGR to RGB
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frames.append(frame_rgb)
                
                frame_number += 1
            
            cap.release()
            logger.info(f"Extracted {len(frames)} frames from video")
            return frames
            
        except Exception as e:
            logger.error(f"Error extracting frames: {str(e)}")
            return []
    
    def analyze_video(self, video_data: bytes, filename: str = "unknown") -> Dict:
        """
        Analyze video file for temporal vegetation patterns.
        """
        try:
            # Save video temporarily for processing
            temp_path = f"/tmp/{filename}"
            with open(temp_path, 'wb') as f:
                f.write(video_data)
            
            # Extract frames
            frames = self.extract_key_frames(temp_path)
            
            if not frames:
                return {
                    'filename': filename,
                    'error': 'No frames could be extracted from video',
                    'success': False
                }
            
            # Analyze each frame
            frame_analyses = []
            for i, frame in enumerate(frames):
                # Convert frame to bytes for analysis
                frame_pil = Image.fromarray(frame)
                frame_bytes = io.BytesIO()
                frame_pil.save(frame_bytes, format='PNG')
                frame_data = frame_bytes.getvalue()
                
                # Analyze frame
                analysis = self.ndvi_analyzer.analyze_image(frame_data, f"{filename}_frame_{i}")
                if 'error' not in analysis:
                    frame_analyses.append(analysis)
            
            # Aggregate results
            if frame_analyses:
                result = self.aggregate_frame_analyses(frame_analyses, filename)
                return result
            else:
                return {
                    'filename': filename,
                    'error': 'No valid frame analyses completed',
                    'success': False
                }
                
        except Exception as e:
            logger.error(f"Error analyzing video {filename}: {str(e)}")
            return {
                'filename': filename,
                'error': str(e),
                'success': False
            }
    
    def aggregate_frame_analyses(self, analyses: List[Dict], filename: str) -> Dict:
        """
        Aggregate multiple frame analyses into a single result.
        """
        try:
            # Calculate averages
            ndvi_means = [a['ndvi_analysis']['mean_ndvi'] for a in analyses]
            vegetation_coverages = [a['vegetation_analysis']['total_vegetation_coverage'] for a in analyses]
            confidence_scores = [a['verification_metrics']['confidence_score'] for a in analyses]
            health_indices = [a['detection_results']['overall_health_index'] for a in analyses]
            
            # Temporal analysis
            vegetation_trend = self.calculate_trend(vegetation_coverages)
            health_trend = self.calculate_trend(health_indices)
            
            result = {
                'filename': filename,
                'timestamp': datetime.now().isoformat(),
                'analysis_type': 'video_temporal',
                'frames_analyzed': len(analyses),
                'temporal_analysis': {
                    'average_ndvi': float(np.mean(ndvi_means)),
                    'average_vegetation_coverage': float(np.mean(vegetation_coverages)),
                    'average_health_index': float(np.mean(health_indices)),
                    'vegetation_stability': float(np.std(vegetation_coverages)),
                    'vegetation_trend': vegetation_trend,
                    'health_trend': health_trend
                },
                'detection_results': {
                    'consistent_mangrove_detection': sum(1 for a in analyses if a['detection_results']['mangrove_detected']) / len(analyses) > 0.5,
                    'temporal_confidence': float(np.mean(confidence_scores))
                },
                'frame_summaries': [a['summary'] for a in analyses[:3]]  # Include first 3 summaries
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error aggregating analyses: {str(e)}")
            return {
                'filename': filename,
                'error': str(e),
                'success': False
            }
    
    def calculate_trend(self, values: List[float]) -> str:
        """
        Calculate trend direction from a series of values.
        """
        if len(values) < 2:
            return "insufficient_data"
        
        # Simple linear regression slope
        x = np.arange(len(values))
        slope = np.polyfit(x, values, 1)[0]
        
        if slope > 1:
            return "increasing"
        elif slope < -1:
            return "decreasing"
        else:
            return "stable"