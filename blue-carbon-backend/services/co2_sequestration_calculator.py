import numpy as np
from typing import Dict, Tuple, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class CO2SequestrationCalculator:
    """
    Advanced CO2 sequestration calculator based on vegetation analysis,
    land transformation, and project area for blue carbon ecosystems.
    """
    
    def __init__(self):
        # Updated carbon sequestration rates split into soil and biomass components
        # Using conservative estimates based on scientific literature (kg CO2/ha/year)
        
        # Soil carbon sequestration rates (more stable, long-term storage)
        self.soil_sequestration_rates = {
            'mangrove': 5000.0,        # Conservative soil carbon rate
            'seagrass': 4500.0,        # High soil carbon in seagrass beds
            'salt_marsh': 5500.0,      # Very high soil carbon accumulation
            'coastal_wetland': 4000.0,  # General coastal soil rate
            'restored_vegetation': 3000.0, # Lower rate for newly restored areas
            'degraded_recovery': 2000.0   # Minimal soil carbon for degraded recovery
        }
        
        # Biomass carbon sequestration rates (above and below ground biomass)
        self.biomass_sequestration_rates = {
            'mangrove': 2000.0,        # High biomass accumulation (7000 total - 5000 soil)
            'seagrass': 500.0,         # Lower biomass (3000 total - 2500 soil, being conservative)
            'salt_marsh': 1500.0,      # Moderate biomass (7000 total - 5500 soil)
            'coastal_wetland': 1000.0,  # General coastal biomass rate
            'restored_vegetation': 800.0, # Lower biomass for newly restored areas
            'degraded_recovery': 500.0   # Minimal biomass for degraded recovery
        }
        
        # Standard restoration rates (kg CO2/ha/year) for verification
        self.standard_restoration_rates = {
            'mangrove': 7000.0,        # 7 t CO₂/ha/yr for mangrove restoration
            'salt_marsh': 7000.0,      # 7 t CO₂/ha/yr for salt marsh restoration  
            'seagrass': 3000.0,        # 3 t CO₂/ha/yr for seagrass restoration
            'coastal_wetland': 4000.0   # Conservative rate for mixed/general wetlands
        }
        
        # Conservative transformation multipliers (capped and reduced)
        self.transformation_multipliers = {
            'barren_to_dense_vegetation': 1.8,    # Reduced from 2.5 (was too high)
            'barren_to_moderate_vegetation': 1.4,  # Reduced from 1.8
            'sparse_to_dense_vegetation': 1.3,    # Reduced from 1.5
            'moderate_to_dense_vegetation': 1.1,  # Reduced from 1.2
            'maintained_vegetation': 1.0,         # Baseline maintenance
            'vegetation_degradation': 0.2,        # Penalty for degradation
            'no_significant_change': 0.6          # Reduced from 0.8 (more conservative)
        }
        
        # Conservative NDVI improvement thresholds and multipliers (capped)
        self.ndvi_thresholds = {
            'excellent': (0.4, 1.5),     # Reduced from 2.0 (cap at 1.5x)
            'very_good': (0.3, 1.3),     # Reduced from 1.7
            'good': (0.2, 1.2),          # Reduced from 1.4
            'moderate': (0.1, 1.1),      # Kept same
            'minimal': (0.05, 0.9),      # Kept same  
            'no_change': (0.0, 0.7)      # Kept same
        }
    
    def detect_ecosystem_type(self, analysis_results: Dict) -> str:
        """
        Detect the type of blue carbon ecosystem based on analysis results.
        """
        try:
            # Check for mangrove indicators
            mangrove_likelihood = analysis_results.get('detection_results', {}).get('mangrove_likelihood', 0)
            water_percentage = analysis_results.get('composition_analysis', {}).get('water_percentage', 0)
            vegetation_coverage = analysis_results.get('vegetation_analysis', {}).get('total_vegetation_coverage', 0)
            
            if mangrove_likelihood > 20 and water_percentage > 10:
                return 'mangrove'
            elif water_percentage > 30 and vegetation_coverage > 40:
                return 'seagrass'
            elif water_percentage > 15 and vegetation_coverage > 50:
                return 'salt_marsh'
            elif water_percentage > 5 and vegetation_coverage > 30:
                return 'coastal_wetland'
            elif vegetation_coverage > 20:
                return 'restored_vegetation'
            else:
                return 'degraded_recovery'
                
        except Exception as e:
            logger.warning(f"Error detecting ecosystem type: {e}")
            return 'coastal_wetland'  # Default to general coastal wetland
    
    def calculate_vegetation_transformation(self, before_analysis: Dict, after_analysis: Dict) -> Dict:
        """
        Calculate vegetation transformation metrics between before and after images.
        """
        try:
            # Extract vegetation coverage percentages
            before_veg = before_analysis.get('vegetation_analysis', {}).get('total_vegetation_coverage', 0)
            after_veg = after_analysis.get('vegetation_analysis', {}).get('total_vegetation_coverage', 0)
            
            # Extract NDVI values
            before_ndvi = before_analysis.get('ndvi_analysis', {}).get('mean_ndvi', 0)
            after_ndvi = after_analysis.get('ndvi_analysis', {}).get('mean_ndvi', 0)
            
            # Extract bare land percentages
            before_bare = before_analysis.get('vegetation_analysis', {}).get('bare_land', 100)
            after_bare = after_analysis.get('vegetation_analysis', {}).get('bare_land', 100)
            
            # Calculate changes
            vegetation_change = after_veg - before_veg
            vegetation_change_percentage = (vegetation_change / max(before_veg, 1)) * 100
            ndvi_improvement = after_ndvi - before_ndvi
            bare_land_reduction = before_bare - after_bare
            
            # Determine transformation type
            transformation_type = self._classify_transformation(
                before_veg, after_veg, before_bare, after_bare, vegetation_change
            )
            
            # Calculate transformation score (0-100)
            transformation_score = self._calculate_transformation_score(
                vegetation_change, ndvi_improvement, bare_land_reduction
            )
            
            return {
                'vegetation_change_absolute': vegetation_change,
                'vegetation_change_percentage': vegetation_change_percentage,
                'ndvi_improvement': ndvi_improvement,
                'bare_land_reduction': bare_land_reduction,
                'transformation_type': transformation_type,
                'transformation_score': transformation_score,
                'before_vegetation_coverage': before_veg,
                'after_vegetation_coverage': after_veg,
                'before_ndvi': before_ndvi,
                'after_ndvi': after_ndvi
            }
            
        except Exception as e:
            logger.error(f"Error calculating vegetation transformation: {e}")
            return {
                'vegetation_change_absolute': 0,
                'vegetation_change_percentage': 0,
                'ndvi_improvement': 0,
                'bare_land_reduction': 0,
                'transformation_type': 'no_significant_change',
                'transformation_score': 0,
                'before_vegetation_coverage': 0,
                'after_vegetation_coverage': 0,
                'before_ndvi': 0,
                'after_ndvi': 0
            }
    
    def _classify_transformation(self, before_veg: float, after_veg: float, 
                                before_bare: float, after_bare: float, veg_change: float) -> str:
        """
        Classify the type of land transformation based on vegetation changes.
        """
        # Significant vegetation increase scenarios
        if veg_change > 30 and before_veg < 20:
            return 'barren_to_dense_vegetation'
        elif veg_change > 20 and before_veg < 30:
            return 'barren_to_moderate_vegetation'
        elif veg_change > 15 and before_veg < 50:
            return 'sparse_to_dense_vegetation'
        elif veg_change > 10 and before_veg >= 30:
            return 'moderate_to_dense_vegetation'
        elif abs(veg_change) <= 5 and after_veg > 40:
            return 'maintained_vegetation'
        elif veg_change < -10:
            return 'vegetation_degradation'
        else:
            return 'no_significant_change'
    
    def _calculate_transformation_score(self, veg_change: float, ndvi_improvement: float, 
                                      bare_reduction: float) -> float:
        """
        Calculate a comprehensive transformation score (0-100).
        """
        try:
            # Weight different factors
            veg_score = min(max(veg_change * 2, 0), 60)  # Max 60 points for vegetation change
            ndvi_score = min(max(ndvi_improvement * 100, 0), 25)  # Max 25 points for NDVI improvement
            bare_score = min(max(bare_reduction * 0.5, 0), 15)  # Max 15 points for bare land reduction
            
            total_score = veg_score + ndvi_score + bare_score
            return min(total_score, 100)  # Cap at 100
            
        except Exception:
            return 0
    
    def _calculate_greenery_change_from_images(self, before_vegetation: Dict, after_vegetation: Dict, 
                                             before_ndvi: Dict, after_ndvi: Dict) -> float:
        """
        Calculate actual greenery change percentage from real image analysis results.
        This is the key enhancement - using REAL image data for calculation.
        """
        try:
            # Get vegetation coverage from REAL image analysis
            before_coverage = before_vegetation.get('total_vegetation_coverage', 
                                                  before_vegetation.get('vegetation_coverage_percentage', 0))
            after_coverage = after_vegetation.get('total_vegetation_coverage', 
                                                after_vegetation.get('vegetation_coverage_percentage', 0))
            
            # Calculate percentage change in vegetation coverage
            if before_coverage == 0:
                # Completely new vegetation - use after coverage directly
                if after_coverage > 0:
                    greenery_change = after_coverage * 2  # Bonus for new vegetation
                else:
                    greenery_change = 0  # No vegetation in either image
            else:
                # Relative improvement/decline
                greenery_change = ((after_coverage - before_coverage) / before_coverage) * 100
            
            # Get NDVI improvement from REAL analysis
            before_ndvi_mean = before_ndvi.get('mean_ndvi', 0)
            after_ndvi_mean = after_ndvi.get('mean_ndvi', 0)
            ndvi_improvement = (after_ndvi_mean - before_ndvi_mean) * 100
            
            # Combine coverage and NDVI changes (weighted average)
            combined_change = (greenery_change * 0.8) + (ndvi_improvement * 0.2)
            
            # CRITICAL: If both images show very low vegetation (barren land), result should be near 0
            if before_coverage < 5 and after_coverage < 5:
                # Barren to barren case - should be 0 or very minimal credits
                if after_coverage <= before_coverage * 1.2:  # Less than 20% relative improvement
                    combined_change = 0  # No meaningful improvement = 0 credits
                else:
                    combined_change = max(0, min(combined_change, 3))  # Cap at 3% for minimal improvement
            elif before_coverage < 10 and after_coverage < 10:
                # Very low vegetation case - cap change
                combined_change = max(0, min(combined_change, 15))  # Cap for low vegetation scenarios
            
            # Cap at reasonable limits
            final_change = max(-50, min(150, combined_change))  # -50% to 150% max change
            
            logger.info(f"REAL IMAGE ANALYSIS: Before coverage: {before_coverage:.1f}%, "
                       f"After coverage: {after_coverage:.1f}%, Final change: {final_change:.1f}%")
            
            return final_change
            
        except Exception as e:
            logger.warning(f"Error calculating greenery change from real images: {e}")
            return 0
    
    def _calculate_greenery_multiplier(self, greenery_change_percentage: float) -> float:
        """
        Convert greenery change percentage to 0-1.5x multiplier for credit calculation.
        CRITICAL: Handles barren-to-barren scenarios with 0x multiplier.
        """
        try:
            if greenery_change_percentage <= -10:
                return 0.0  # Vegetation loss = no credits
            elif greenery_change_percentage <= 0:
                return 0.0  # No improvement = no credits
            elif greenery_change_percentage <= 10:
                return 0.05  # Very minimal improvement (barren-to-barren case)
            elif greenery_change_percentage <= 20:
                return 0.2  # Minimal improvement
            elif greenery_change_percentage <= 35:
                return 0.5  # Moderate improvement  
            elif greenery_change_percentage <= 50:
                return 0.8  # Good improvement
            elif greenery_change_percentage <= 75:
                return 1.1  # Very good improvement
            elif greenery_change_percentage <= 100:
                return 1.3  # Excellent improvement
            else:
                return 1.5  # Outstanding improvement (capped at 1.5x)
                
        except Exception:
            return 0.0  # Safe fallback for errors
    
    def calculate_co2_sequestration(self, before_analysis: Dict, after_analysis: Dict, 
                                  project_area_hectares: float, 
                                  time_period_years: float = 1.0,
                                  area_fraction_transformed: float = 1.0) -> Dict:
        """
        Calculate CO2 sequestration with enhanced image-based greenery change multiplier.
        Now uses actual vegetation change from before/after image analysis as primary multiplier.
        """
        try:
            # Extract vegetation metrics from image analysis (FIX: correct field mapping)
            before_vegetation = before_analysis.get('vegetation_analysis', {})
            after_vegetation = after_analysis.get('vegetation_analysis', {})
            
            # Also get NDVI data
            before_ndvi = before_analysis.get('ndvi_analysis', {})
            after_ndvi = after_analysis.get('ndvi_analysis', {})
            
            # ENHANCED: Calculate actual greenery change from images (0-1.5x multiplier)
            greenery_change_percentage = self._calculate_greenery_change_from_images(
                before_vegetation, after_vegetation, before_ndvi, after_ndvi
            )
            greenery_multiplier = self._calculate_greenery_multiplier(greenery_change_percentage)
            
            # Calculate transformation metrics (for additional context)
            transformation = self.calculate_vegetation_transformation(before_analysis, after_analysis)
            
            # Detect ecosystem type from after analysis (assuming improvement)
            ecosystem_type = self.detect_ecosystem_type(after_analysis)
            
            # Get base sequestration rates (separated into soil and biomass)
            soil_rate = self.soil_sequestration_rates.get(ecosystem_type, 4000.0)
            biomass_rate = self.biomass_sequestration_rates.get(ecosystem_type, 500.0)
            
            # Apply conservative transformation multiplier (reduced impact since greenery is primary)
            transformation_multiplier = self.transformation_multipliers.get(
                transformation['transformation_type'], 0.6
            ) * 0.5  # Reduced since greenery multiplier is now primary
            
            # Calculate area factor with conservative approach
            area_factor = self._calculate_area_factor(project_area_hectares)
            
            # Apply area fraction transformed
            effective_area = project_area_hectares * area_fraction_transformed
            
            # Calculate soil carbon sequestration (stable component, use greenery multiplier)
            soil_co2_sequestration = (
                soil_rate * 
                transformation_multiplier * 
                greenery_multiplier *  # PRIMARY: Use image-based greenery change
                area_factor * 
                effective_area * 
                time_period_years
            )
            
            # Calculate biomass carbon sequestration (variable component, enhanced greenery impact)
            biomass_co2_sequestration = (
                biomass_rate * 
                transformation_multiplier * 
                greenery_multiplier * 1.2 *  # Enhanced impact for biomass
                area_factor * 
                effective_area * 
                time_period_years
            )
            
            # Total CO2 sequestration
            total_co2_sequestration = soil_co2_sequestration + biomass_co2_sequestration
            
            # Apply confidence adjustment based on analysis quality
            confidence_factor = self._calculate_confidence_factor(before_analysis, after_analysis)
            adjusted_co2_sequestration = total_co2_sequestration * confidence_factor
            
            # Calculate standard rate comparison for verification
            standard_rate = self.standard_restoration_rates.get(ecosystem_type, 4000.0)
            standard_co2 = standard_rate * effective_area * time_period_years
            
            return {
                'co2_sequestration_kg': round(adjusted_co2_sequestration, 2),
                'co2_sequestration_tonnes': round(adjusted_co2_sequestration / 1000, 3),
                'soil_co2_kg': round(soil_co2_sequestration * confidence_factor, 2),
                'biomass_co2_kg': round(biomass_co2_sequestration * confidence_factor, 2),
                'standard_rate_co2_kg': round(standard_co2, 2),
                
                # Enhanced image-based analysis results
                'greenery_change_percentage': greenery_change_percentage,
                'greenery_multiplier': greenery_multiplier,
                
                # Ecosystem and rates
                'ecosystem_type': ecosystem_type,
                'soil_rate_kg_ha_year': soil_rate,
                'biomass_rate_kg_ha_year': biomass_rate,
                'standard_rate_kg_ha_year': standard_rate,
                
                # Calculation factors
                'transformation_multiplier': transformation_multiplier,
                'area_factor': area_factor,
                'confidence_factor': confidence_factor,
                'area_fraction_transformed': area_fraction_transformed,
                'effective_area_hectares': effective_area,
                'project_area_hectares': project_area_hectares,
                'time_period_years': time_period_years,
                'transformation_metrics': transformation,
                
                # Method identification
                'calculation_method': 'image_based_greenery_analysis'
            }
            
        except Exception as e:
            logger.error(f"Error calculating CO2 sequestration: {e}")
            return {
                'co2_sequestration_kg': 0,
                'co2_sequestration_tonnes': 0,
                'soil_co2_kg': 0,
                'biomass_co2_kg': 0,
                'standard_rate_co2_kg': 0,
                'ecosystem_type': 'unknown',
                'soil_rate_kg_ha_year': 0,
                'biomass_rate_kg_ha_year': 0,
                'standard_rate_kg_ha_year': 0,
                'transformation_multiplier': 0,
                'ndvi_multiplier': 0,
                'area_factor': 0,
                'confidence_factor': 0,
                'area_fraction_transformed': area_fraction_transformed,
                'effective_area_hectares': 0,
                'project_area_hectares': project_area_hectares,
                'time_period_years': time_period_years,
                'transformation_metrics': {}
            }
    
    def _get_ndvi_multiplier(self, ndvi_improvement: float) -> float:
        """
        Get NDVI improvement multiplier based on improvement value.
        """
        for level, (threshold, multiplier) in self.ndvi_thresholds.items():
            if ndvi_improvement >= threshold:
                return multiplier
        return 0.7  # Default for no improvement
    
    def _calculate_area_factor(self, hectares: float) -> float:
        """
        Calculate area factor that adjusts sequestration based on project size.
        """
        if hectares <= 0:
            return 0
        elif hectares < 1:
            return 0.8  # Small areas may have edge effects
        elif hectares <= 10:
            return 1.0  # Optimal size
        elif hectares <= 50:
            return 1.1  # Good economies of scale
        elif hectares <= 100:
            return 1.05  # Some economies of scale
        else:
            return 1.0  # Large areas may have management challenges
    
    def _calculate_confidence_factor(self, before_analysis: Dict, after_analysis: Dict) -> float:
        """
        Calculate confidence factor based on analysis quality.
        """
        try:
            before_confidence = before_analysis.get('verification_metrics', {}).get('confidence_score', 70)
            after_confidence = after_analysis.get('verification_metrics', {}).get('confidence_score', 70)
            
            avg_confidence = (before_confidence + after_confidence) / 2
            
            # Convert confidence percentage to factor (0.6 to 1.0)
            confidence_factor = 0.6 + (avg_confidence / 100) * 0.4
            
            return min(max(confidence_factor, 0.6), 1.0)
            
        except Exception:
            return 0.8  # Default confidence factor
    
    def calculate_carbon_credits(self, co2_sequestration_kg: float, 
                               credit_conversion_rate: float = 0.1) -> Dict:
        """
        Calculate carbon credits based on CO2 sequestration.
        Default conversion: 1 carbon credit per 10 kg CO2 sequestered.
        """
        try:
            # Convert kg to tonnes for standard carbon credit calculation
            co2_tonnes = co2_sequestration_kg / 1000
            
            # Calculate credits (typically 1 credit = 1 tonne CO2, but adjustable)
            # Using conversion rate to make credits more granular for smaller projects
            carbon_credits = co2_tonnes / credit_conversion_rate
            
            return {
                'carbon_credits': round(carbon_credits, 2),
                'co2_tonnes': round(co2_tonnes, 3),
                'credit_conversion_rate': credit_conversion_rate,
                'calculation_method': 'ai_based_sequestration'
            }
            
        except Exception as e:
            logger.error(f"Error calculating carbon credits: {e}")
            return {
                'carbon_credits': 0,
                'co2_tonnes': 0,
                'credit_conversion_rate': credit_conversion_rate,
                'calculation_method': 'error'
            }

    def calculate_basic_co2_sequestration(self, ecosystem_type: str, 
                                        area_hectares: float, 
                                        time_period_years: float = 1.0, 
                                        transformation_factor: float = 1.0,
                                        area_fraction_transformed: float = 1.0) -> float:
        """
        Calculate basic CO2 sequestration without image analysis.
        Now uses conservative standard restoration rates.
        
        Args:
            ecosystem_type: Type of ecosystem ('mangrove', 'seagrass', 'saltmarsh', 'mixed')
            area_hectares: Project area in hectares
            time_period_years: Time period for calculation
            transformation_factor: Estimated transformation impact (0.5-1.5, capped)
            area_fraction_transformed: Fraction of area actually transformed (0.0-1.0)
        
        Returns:
            CO2 sequestration in kg
        """
        try:
            # Map ecosystem types to standard restoration rates
            ecosystem_mapping = {
                'mangrove': 'mangrove',        # 7000 kg/ha/yr
                'seagrass': 'seagrass',        # 3000 kg/ha/yr
                'saltmarsh': 'salt_marsh',     # 7000 kg/ha/yr
                'mixed': 'coastal_wetland'     # 4000 kg/ha/yr (conservative)
            }
            
            internal_type = ecosystem_mapping.get(ecosystem_type, 'coastal_wetland')
            standard_rate = self.standard_restoration_rates.get(internal_type, 4000.0)
            
            # Cap transformation factor to be more conservative
            capped_transformation_factor = min(max(transformation_factor, 0.5), 1.5)
            
            # Apply area factor with conservative approach
            area_factor = self._calculate_area_factor(area_hectares)
            
            # Calculate effective area based on transformation fraction
            effective_area = area_hectares * area_fraction_transformed
            
            # Calculate basic sequestration using standard rates
            co2_sequestration = (standard_rate * capped_transformation_factor * 
                               area_factor * effective_area * time_period_years)
            
            return max(0, co2_sequestration)
            
        except Exception as e:
            logger.error(f"Error in basic CO2 calculation: {e}")
            return 0.0

    @property
    def base_rates(self) -> Dict[str, float]:
        """Return standard restoration rates for external access"""
        return {
            'mangrove': self.standard_restoration_rates['mangrove'],      # 7000 kg/ha/yr
            'seagrass': self.standard_restoration_rates['seagrass'],      # 3000 kg/ha/yr
            'saltmarsh': self.standard_restoration_rates['salt_marsh'],   # 7000 kg/ha/yr
            'mixed': self.standard_restoration_rates['coastal_wetland']   # 4000 kg/ha/yr
        }