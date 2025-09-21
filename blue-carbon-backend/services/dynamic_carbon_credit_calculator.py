from typing import Dict, Optional, Tuple, List
import logging
from datetime import datetime
from .ai_verification import BeforeAfterAnalyzer
from .co2_sequestration_calculator import CO2SequestrationCalculator

logger = logging.getLogger(__name__)

class DynamicCarbonCreditCalculator:
    """
    Dynamic carbon credit calculator that integrates AI analysis results
    to determine carbon credits based on actual vegetation transformation
    and CO2 sequestration potential.
    """
    
    def __init__(self):
        self.before_after_analyzer = BeforeAfterAnalyzer()
        self.co2_calculator = CO2SequestrationCalculator()
        
        # Updated credit calculation settings with provisional credit system
        self.settings = {
            'min_credits_per_project': 0.5,     # Reduced minimum credits
            'max_credits_per_hectare': 35.0,    # Reduced maximum (was 50.0)
            'baseline_credit_rate': 0.1,        # Base conversion rate (1 credit per 10kg CO2)
            'quality_bonus_multiplier': 1.2,    # Reduced bonus (was 1.5)
            'verification_confidence_threshold': 70.0,  # Increased threshold (was 60.0)
            'enable_bonus_credits': True,       
            'enable_fractional_credits': True,
            
            # Provisional credit system settings
            'enable_provisional_credits': True,
            'provisional_credit_percentage': 0.5,  # Issue 50% immediately
            'provisional_verification_period_years': 3,  # Verify remainder after 3 years
            'strict_confidence_threshold': 85.0,  # High confidence required for full credits
            'minimum_monitoring_period_months': 12  # Minimum monitoring period
        }
    
    def calculate_dynamic_credits(self, before_image_data: bytes, after_image_data: bytes,
                                project_area_hectares: float, time_period_years: float = 1.0,
                                project_metadata: Optional[Dict] = None) -> Dict:
        """
        Calculate dynamic carbon credits based on before/after image analysis.
        """
        try:
            logger.info(f"Calculating dynamic credits for {project_area_hectares} hectare project")
            
            # Perform comprehensive before/after analysis
            analysis_result = self.before_after_analyzer.compare_images(
                before_image_data, after_image_data, project_area_hectares, time_period_years
            )
            
            if not analysis_result.get('success', False):
                return {
                    'success': False,
                    'error': analysis_result.get('error', 'Analysis failed'),
                    'recommended_credits': 0,
                    'calculation_method': 'failed'
                }
            
            # Extract key metrics from analysis
            transformation_metrics = analysis_result.get('transformation_metrics', {})
            co2_results = analysis_result.get('co2_sequestration', {})
            verification_score = analysis_result.get('verification_score', {})
            
            # Calculate base credits from CO2 sequestration
            base_credits = self._calculate_base_credits(co2_results)
            
            # Apply quality adjustments
            adjusted_credits = self._apply_quality_adjustments(
                base_credits, transformation_metrics, verification_score
            )
            
            # Apply project-specific bonuses
            final_credits = self._apply_project_bonuses(
                adjusted_credits, transformation_metrics, project_area_hectares, project_metadata
            )
            
            # Validate and constrain credits
            validated_credits = self._validate_and_constrain_credits(
                final_credits, project_area_hectares, verification_score
            )
            
            # Calculate provisional credit distribution
            credit_distribution = self._calculate_provisional_credits(
                validated_credits, verification_score, transformation_metrics
            )
            
            # Generate credit calculation summary
            calculation_summary = self._generate_calculation_summary(
                base_credits, adjusted_credits, final_credits, validated_credits,
                transformation_metrics, co2_results, verification_score
            )
            
            # Prepare final result
            result = {
                'success': True,
                'timestamp': datetime.now().isoformat(),
                'recommended_credits': credit_distribution['total_credits'],
                'provisional_credits': credit_distribution['provisional_credits'],
                'deferred_credits': credit_distribution['deferred_credits'],
                'calculation_method': 'ai_dynamic_analysis_provisional',
                'project_area_hectares': project_area_hectares,
                'time_period_years': time_period_years,
                
                # Credit calculation breakdown
                'credit_breakdown': {
                    'base_credits': base_credits,
                    'quality_adjusted_credits': adjusted_credits,
                    'bonus_adjusted_credits': final_credits,
                    'final_validated_credits': validated_credits
                },
                
                # Provisional credit system
                'credit_distribution': credit_distribution,
                'monitoring_requirements': credit_distribution.get('monitoring_requirements', []),
                
                # Supporting analysis
                'supporting_analysis': {
                    **analysis_result,
                    'vegetation_change_multiplier': analysis_result.get('vegetation_change_multiplier', {}),
                    'transformation_metrics': analysis_result.get('transformation_metrics', {}),
                    'co2_sequestration': analysis_result.get('co2_sequestration', {}),
                    'carbon_credits': analysis_result.get('carbon_credits', {})
                },
                'calculation_summary': calculation_summary,
                
                # Verification information
                'verification_confidence': verification_score.get('overall_verification_score', 0),
                'verification_level': verification_score.get('verification_level', 'unknown'),
                'recommended_action': verification_score.get('recommended_action', 'review_required'),
                
                # Transparency metrics
                'calculation_factors': self._get_calculation_factors(
                    transformation_metrics, co2_results, verification_score
                )
            }
            
            logger.info(f"Dynamic credit calculation completed. Provisional: {credit_distribution['provisional_credits']:.2f}, Deferred: {credit_distribution['deferred_credits']:.2f} credits")
            return result
            
        except Exception as e:
            logger.error(f"Error in dynamic credit calculation: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'recommended_credits': 0,
                'provisional_credits': 0,
                'deferred_credits': 0,
                'calculation_method': 'error',
                'timestamp': datetime.now().isoformat()
            }
    
    def _calculate_base_credits(self, co2_results: Dict) -> float:
        """
        Calculate base carbon credits from CO2 sequestration results.
        """
        try:
            co2_kg = co2_results.get('co2_sequestration_kg', 0)
            
            # Convert CO2 to credits using baseline rate
            base_credits = co2_kg * self.settings['baseline_credit_rate']
            
            # Ensure minimum credits for valid projects
            if co2_kg > 0:
                base_credits = max(base_credits, self.settings['min_credits_per_project'])
            
            return base_credits
            
        except Exception as e:
            logger.error(f"Error calculating base credits: {e}")
            return 0
    
    def _apply_quality_adjustments(self, base_credits: float, transformation_metrics: Dict,
                                 verification_score: Dict) -> float:
        """
        Apply quality-based adjustments to base credits.
        """
        try:
            # Start with base credits
            adjusted_credits = base_credits
            
            # Quality multiplier based on transformation quality
            transformation_quality = transformation_metrics.get('transformation_quality', 'poor')
            quality_multipliers = {
                'excellent': 1.3,
                'very_good': 1.2,
                'good': 1.1,
                'moderate': 1.0,
                'minimal': 0.9,
                'poor': 0.7
            }
            quality_multiplier = quality_multipliers.get(transformation_quality, 0.8)
            adjusted_credits *= quality_multiplier
            
            # Confidence-based adjustment
            confidence_score = verification_score.get('overall_verification_score', 70)
            if confidence_score < self.settings['verification_confidence_threshold']:
                confidence_penalty = confidence_score / self.settings['verification_confidence_threshold']
                adjusted_credits *= confidence_penalty
            elif confidence_score > 90:
                # High confidence bonus
                adjusted_credits *= 1.1
            
            # NDVI improvement bonus
            ndvi_improvement = transformation_metrics.get('ndvi_improvement', 0)
            if ndvi_improvement > 0.3:
                adjusted_credits *= 1.15  # Significant NDVI improvement bonus
            elif ndvi_improvement > 0.2:
                adjusted_credits *= 1.08  # Good NDVI improvement bonus
            
            return adjusted_credits
            
        except Exception as e:
            logger.error(f"Error applying quality adjustments: {e}")
            return base_credits
    
    def _validate_and_constrain_credits(self, final_credits: float, project_area_hectares: float, 
                                      verification_score: Dict) -> float:
        """
        Validate and constrain credits within acceptable limits.
        """
        try:
            # Apply minimum credit threshold
            min_credits = self.settings['min_credits_per_project']
            validated_credits = max(final_credits, min_credits)
            
            # Apply maximum credit per hectare limit
            max_credits_total = project_area_hectares * self.settings['max_credits_per_hectare']
            validated_credits = min(validated_credits, max_credits_total)
            
            # Apply confidence-based constraints
            confidence_score = verification_score.get('overall_verification_score', 70)
            confidence_threshold = self.settings['verification_confidence_threshold']
            
            if confidence_score < confidence_threshold:
                # Reduce credits for low confidence
                confidence_multiplier = max(0.5, confidence_score / confidence_threshold)
                validated_credits *= confidence_multiplier
                logger.info(f"Applied confidence reduction: {confidence_multiplier:.2f}x due to low verification score")
            
            # Ensure positive credits
            validated_credits = max(0, validated_credits)
            
            logger.info(f"Credits validated: {final_credits:.2f} -> {validated_credits:.2f}")
            return validated_credits
            
        except Exception as e:
            logger.error(f"Error validating and constraining credits: {e}")
            return max(0, final_credits)  # Return non-negative fallback
    
    def _apply_project_bonuses(self, credits: float, transformation_metrics: Dict,
                             project_area_hectares: float, project_metadata: Optional[Dict]) -> float:
        """
        Apply project-specific bonuses for exceptional cases.
        """
        try:
            if not self.settings['enable_bonus_credits']:
                return credits
            
            bonus_credits = credits
            
            # Exceptional transformation bonus
            transformation_score = transformation_metrics.get('transformation_score', 0)
            if transformation_score > 85:
                bonus_credits *= 1.2  # Exceptional transformation bonus
            
            # Ecosystem restoration bonus
            land_use_change = transformation_metrics.get('land_use_change', {})
            if land_use_change.get('is_restoration_project', False):
                bonus_credits *= 1.15  # Restoration project bonus
            
            # Large-scale project efficiency bonus
            if project_area_hectares > 20:
                scale_bonus = min(1.1, 1 + (project_area_hectares - 20) * 0.002)
                bonus_credits *= scale_bonus
            
            # Ecosystem type bonus (if metadata available)
            if project_metadata:
                ecosystem_type = project_metadata.get('ecosystem_type', '')
                if ecosystem_type.lower() in ['mangrove', 'salt_marsh']:
                    bonus_credits *= 1.1  # High-value ecosystem bonus
            
            # Biodiversity improvement bonus
            vegetation_details = transformation_metrics.get('vegetation_details', {})
            healthy_veg_increase = vegetation_details.get('healthy_vegetation_change', 0)
            if healthy_veg_increase > 30:
                bonus_credits *= 1.1  # Significant biodiversity improvement
            
            return bonus_credits
            
        except Exception as e:
            logger.error(f"Error applying project bonuses: {e}")
            return credits
    
    def _calculate_provisional_credits(self, validated_credits: float, verification_score: Dict,
                                     transformation_metrics: Dict) -> Dict:
        """
        Calculate provisional credit distribution with deferred credits for long-term verification.
        """
        try:
            # Determine confidence level
            confidence = verification_score.get('overall_verification_score', 0)
            verification_level = verification_score.get('verification_level', 'low')
            
            # Calculate provisional percentage based on confidence
            if confidence >= self.settings['strict_confidence_threshold'] and verification_level in ['high', 'very_high']:
                provisional_percentage = self.settings['provisional_credit_percentage']
            elif confidence >= 70:
                provisional_percentage = self.settings['provisional_credit_percentage'] * 0.8  # 40%
            elif confidence >= 60:
                provisional_percentage = self.settings['provisional_credit_percentage'] * 0.6  # 30%
            else:
                provisional_percentage = self.settings['provisional_credit_percentage'] * 0.4  # 20%
            
            # Calculate credit distribution
            provisional_credits = validated_credits * provisional_percentage
            deferred_credits = validated_credits - provisional_credits
            
            # Generate monitoring requirements
            monitoring_requirements = self._generate_monitoring_requirements(
                verification_score, transformation_metrics, validated_credits
            )
            
            return {
                'total_credits': validated_credits,
                'provisional_credits': provisional_credits,
                'deferred_credits': deferred_credits,
                'provisional_percentage': provisional_percentage,
                'verification_period_years': self.settings['provisional_verification_period_years'],
                'monitoring_requirements': monitoring_requirements,
                'release_schedule': {
                    'immediate': provisional_credits,
                    f'year_{self.settings["provisional_verification_period_years"]}': deferred_credits
                }
            }
            
        except Exception as e:
            logger.error(f"Error calculating provisional credits: {e}")
            return {
                'total_credits': validated_credits,
                'provisional_credits': validated_credits * 0.2,  # Conservative fallback
                'deferred_credits': validated_credits * 0.8,
                'provisional_percentage': 0.2,
                'verification_period_years': self.settings['provisional_verification_period_years'],
                'monitoring_requirements': ["Enhanced monitoring required due to calculation error"],
                'release_schedule': {
                    'immediate': validated_credits * 0.2,
                    f'year_{self.settings["provisional_verification_period_years"]}': validated_credits * 0.8
                },
                'error': str(e)
            }
    
    def _generate_monitoring_requirements(self, verification_score: Dict, 
                                        transformation_metrics: Dict, 
                                        total_credits: float) -> List[str]:
        """
        Generate specific monitoring requirements based on project characteristics.
        """
        requirements = []
        
        # Base monitoring requirements
        requirements.append("Annual satellite imagery verification")
        requirements.append("Ground-truth validation within 18 months")
        
        # Confidence-based requirements
        confidence = verification_score.get('overall_verification_score', 0)
        if confidence < 80:
            requirements.append("Quarterly progress reports with photographic evidence")
            requirements.append("Independent third-party verification required")
        
        # High-value project requirements
        if total_credits > 1000:
            requirements.append("Continuous remote sensing monitoring")
            requirements.append("Annual on-site inspection")
        
        # Project-specific requirements
        transformation_quality = transformation_metrics.get('transformation_quality', 'poor')
        if transformation_quality in ['minimal', 'poor']:
            requirements.append("Enhanced monitoring with monthly updates")
            requirements.append("Corrective action plan if progress stalls")
        
        # Minimum period requirement
        requirements.append(f"Minimum {self.settings['minimum_monitoring_period_months']} month monitoring period")
        
        return requirements
        """
        Validate and constrain credits within reasonable bounds.
        """
        try:
            # Apply minimum credits
            validated_credits = max(credits, 0)
            
            # Apply maximum credits per hectare constraint
            max_total_credits = project_area_hectares * self.settings['max_credits_per_hectare']
            validated_credits = min(validated_credits, max_total_credits)
            
            # Verification confidence-based capping
            confidence_score = verification_score.get('overall_verification_score', 70)
            if confidence_score < 70:
                # Cap credits for low confidence projects
                max_low_confidence_credits = project_area_hectares * 10  # Conservative cap
                validated_credits = min(validated_credits, max_low_confidence_credits)
            
            # Round to appropriate precision
            if self.settings['enable_fractional_credits']:
                validated_credits = round(validated_credits, 2)
            else:
                validated_credits = round(validated_credits)
            
            # Ensure minimum for valid projects
            if credits > 0 and validated_credits < self.settings['min_credits_per_project']:
                validated_credits = self.settings['min_credits_per_project']
            
            return validated_credits
            
        except Exception as e:
            logger.error(f"Error validating credits: {e}")
            return 0
    
    def _generate_calculation_summary(self, base_credits: float, adjusted_credits: float,
                                    final_credits: float, validated_credits: float,
                                    transformation_metrics: Dict, co2_results: Dict,
                                    verification_score: Dict) -> str:
        """
        Generate a human-readable summary of the credit calculation process.
        """
        try:
            summary_parts = []
            
            # Header
            summary_parts.append("CARBON CREDIT CALCULATION SUMMARY")
            summary_parts.append("=" * 40)
            
            # Base calculation
            co2_kg = co2_results.get('co2_sequestration_kg', 0)
            summary_parts.append(f"1. Base Calculation:")
            summary_parts.append(f"   • CO₂ Sequestration: {co2_kg:.1f} kg")
            summary_parts.append(f"   • Base Credits: {base_credits:.2f}")
            
            # Quality adjustments
            quality = transformation_metrics.get('transformation_quality', 'unknown')
            confidence = verification_score.get('overall_verification_score', 0)
            summary_parts.append(f"2. Quality Adjustments:")
            summary_parts.append(f"   • Transformation Quality: {quality.title()}")
            summary_parts.append(f"   • Verification Confidence: {confidence:.1f}%")
            summary_parts.append(f"   • Quality Adjusted Credits: {adjusted_credits:.2f}")
            
            # Bonuses
            if final_credits > adjusted_credits:
                summary_parts.append(f"3. Project Bonuses Applied:")
                summary_parts.append(f"   • Bonus Adjusted Credits: {final_credits:.2f}")
            
            # Final validation
            summary_parts.append(f"4. Final Validation:")
            summary_parts.append(f"   • Validated Credits: {validated_credits:.2f}")
            
            # Recommendation
            action = verification_score.get('recommended_action', 'review_required')
            summary_parts.append(f"5. Recommendation: {action.replace('_', ' ').title()}")
            
            return "\n".join(summary_parts)
            
        except Exception as e:
            logger.error(f"Error generating calculation summary: {e}")
            return "Credit calculation summary unavailable due to processing error."
    
    def _get_calculation_factors(self, transformation_metrics: Dict, co2_results: Dict,
                               verification_score: Dict) -> Dict:
        """
        Get detailed calculation factors for transparency.
        """
        try:
            return {
                'co2_sequestration_kg': co2_results.get('co2_sequestration_kg', 0),
                'base_credit_rate': self.settings['baseline_credit_rate'],
                'transformation_quality': transformation_metrics.get('transformation_quality', 'unknown'),
                'transformation_score': transformation_metrics.get('transformation_score', 0),
                'vegetation_change_percentage': transformation_metrics.get('vegetation_change_percentage', 0),
                'ndvi_improvement': transformation_metrics.get('ndvi_improvement', 0),
                'verification_confidence': verification_score.get('overall_verification_score', 0),
                'ecosystem_type': co2_results.get('ecosystem_type', 'unknown'),
                'confidence_factor': co2_results.get('confidence_factor', 0),
                'area_factor': co2_results.get('area_factor', 0),
                'transformation_multiplier': co2_results.get('transformation_multiplier', 0),
                'ndvi_multiplier': co2_results.get('ndvi_multiplier', 0)
            }
        except Exception as e:
            logger.error(f"Error getting calculation factors: {e}")
            return {}
    
    def calculate_legacy_credits(self, project_area_hectares: float) -> Dict:
        """
        Calculate credits using the legacy fixed-rate method (100 credits per project).
        """
        try:
            # Legacy method: fixed 100 credits regardless of size or transformation
            legacy_credits = 100.0
            
            return {
                'success': True,
                'recommended_credits': legacy_credits,
                'calculation_method': 'legacy_fixed',
                'project_area_hectares': project_area_hectares,
                'calculation_summary': f"Legacy calculation: Fixed {legacy_credits} credits per project",
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in legacy credit calculation: {e}")
            return {
                'success': False,
                'error': str(e),
                'recommended_credits': 0,
                'calculation_method': 'legacy_error'
            }
    
    def update_settings(self, new_settings: Dict) -> Dict:
        """
        Update calculator settings.
        """
        try:
            original_settings = self.settings.copy()
            
            # Update settings with validation
            for key, value in new_settings.items():
                if key in self.settings:
                    self.settings[key] = value
                else:
                    logger.warning(f"Unknown setting: {key}")
            
            return {
                'success': True,
                'message': 'Settings updated successfully',
                'original_settings': original_settings,
                'updated_settings': self.settings
            }
            
        except Exception as e:
            logger.error(f"Error updating settings: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to update settings'
            }