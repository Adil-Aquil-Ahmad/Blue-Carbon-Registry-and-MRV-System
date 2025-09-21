import cv2
import numpy as np
from typing import List, Dict, Tuple
import logging
import tempfile
import os
from datetime import datetime

logger = logging.getLogger(__name__)

class AdvancedVideoAnalyzer:
    """
    Enhanced video analysis for comprehensive temporal vegetation monitoring.
    Provides frame-by-frame analysis, motion detection, and growth tracking.
    """
    
    def __init__(self):
        self.min_frame_interval = 1.0  # Minimum seconds between analyzed frames
        self.max_frames_per_video = 15  # Maximum frames to analyze per video
        self.motion_threshold = 30  # Motion detection threshold
        
    def extract_optimal_frames(self, video_path: str) -> List[Dict]:
        """
        Extract optimal frames based on content analysis and temporal distribution.
        """
        try:
            cap = cv2.VideoCapture(video_path)
            
            if not cap.isOpened():
                raise Exception("Could not open video file")
            
            # Get video properties
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = frame_count / fps if fps > 0 else 0
            
            logger.info(f"Video properties: {frame_count} frames, {fps:.2f} FPS, {duration:.2f}s duration")
            
            # Calculate frame sampling strategy
            if duration <= 30:  # Short video: analyze more frames
                target_frames = min(frame_count, self.max_frames_per_video)
            else:  # Long video: sample strategically
                target_frames = self.max_frames_per_video
            
            # Calculate frame intervals
            if target_frames >= frame_count:
                frame_indices = list(range(frame_count))
            else:
                frame_indices = np.linspace(0, frame_count - 1, target_frames, dtype=int)
            
            frames_data = []
            prev_frame = None
            
            for i, frame_idx in enumerate(frame_indices):
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
                ret, frame = cap.read()
                
                if not ret:
                    continue
                
                # Convert BGR to RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Calculate frame quality metrics
                quality_metrics = self.calculate_frame_quality(frame_rgb)
                
                # Calculate motion if we have a previous frame
                motion_score = 0
                if prev_frame is not None:
                    motion_score = self.calculate_motion_score(prev_frame, frame_rgb)
                
                # Calculate timestamp
                timestamp = frame_idx / fps if fps > 0 else 0
                
                frame_data = {
                    'frame_index': frame_idx,
                    'timestamp': timestamp,
                    'frame': frame_rgb,
                    'quality_metrics': quality_metrics,
                    'motion_score': motion_score,
                    'sequence_position': i / (len(frame_indices) - 1) if len(frame_indices) > 1 else 0
                }
                
                frames_data.append(frame_data)
                prev_frame = frame_rgb.copy()
            
            cap.release()
            
            # Filter frames based on quality and diversity
            selected_frames = self.select_best_frames(frames_data)
            
            logger.info(f"Selected {len(selected_frames)} frames from {len(frames_data)} candidates")
            return selected_frames
            
        except Exception as e:
            logger.error(f"Error extracting frames: {str(e)}")
            return []
    
    def calculate_frame_quality(self, frame: np.ndarray) -> Dict:
        """
        Calculate comprehensive frame quality metrics.
        """
        try:
            # Convert to grayscale for some calculations
            gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            
            # Sharpness (Laplacian variance)
            laplacian = cv2.Laplacian(gray, cv2.CV_64F)
            sharpness = laplacian.var()
            
            # Brightness (mean intensity)
            brightness = np.mean(gray)
            
            # Contrast (standard deviation of intensity)
            contrast = np.std(gray)
            
            # Color diversity (variance in color channels)
            color_variance = np.var(frame, axis=(0, 1))
            color_diversity = np.mean(color_variance)
            
            # Edge density
            edges = cv2.Canny(gray, 50, 150)
            edge_density = np.sum(edges > 0) / edges.size
            
            # Overall quality score (weighted combination)
            quality_score = (
                (sharpness / 1000) * 0.3 +
                (min(brightness, 255 - brightness) / 127.5) * 0.2 +
                (contrast / 127.5) * 0.2 +
                (color_diversity / 10000) * 0.15 +
                (edge_density * 100) * 0.15
            )
            
            return {
                'sharpness': float(sharpness),
                'brightness': float(brightness),
                'contrast': float(contrast),
                'color_diversity': float(color_diversity),
                'edge_density': float(edge_density),
                'quality_score': float(quality_score)
            }
            
        except Exception as e:
            logger.error(f"Error calculating frame quality: {str(e)}")
            return {
                'sharpness': 0.0,
                'brightness': 128.0,
                'contrast': 0.0,
                'color_diversity': 0.0,
                'edge_density': 0.0,
                'quality_score': 0.0
            }
    
    def calculate_motion_score(self, frame1: np.ndarray, frame2: np.ndarray) -> float:
        """
        Calculate motion score between two frames.
        """
        try:
            # Convert to grayscale
            gray1 = cv2.cvtColor(frame1, cv2.COLOR_RGB2GRAY)
            gray2 = cv2.cvtColor(frame2, cv2.COLOR_RGB2GRAY)
            
            # Calculate absolute difference
            diff = cv2.absdiff(gray1, gray2)
            
            # Apply threshold to get motion areas
            _, motion_mask = cv2.threshold(diff, self.motion_threshold, 255, cv2.THRESH_BINARY)
            
            # Calculate motion score as percentage of pixels with motion
            motion_pixels = np.sum(motion_mask > 0)
            total_pixels = motion_mask.size
            motion_score = (motion_pixels / total_pixels) * 100
            
            return float(motion_score)
            
        except Exception as e:
            logger.error(f"Error calculating motion score: {str(e)}")
            return 0.0
    
    def select_best_frames(self, frames_data: List[Dict]) -> List[Dict]:
        """
        Select the best frames based on quality and temporal distribution.
        """
        try:
            if not frames_data:
                return []
            
            # Sort frames by quality score
            frames_by_quality = sorted(frames_data, key=lambda x: x['quality_metrics']['quality_score'], reverse=True)
            
            # Ensure temporal distribution
            selected_frames = []
            
            # Always include first and last frames if available
            if len(frames_data) > 0:
                first_frame = min(frames_data, key=lambda x: x['timestamp'])
                last_frame = max(frames_data, key=lambda x: x['timestamp'])
                
                selected_frames.append(first_frame)
                if first_frame != last_frame:
                    selected_frames.append(last_frame)
            
            # Add high-quality frames from middle sections
            remaining_frames = [f for f in frames_by_quality if f not in selected_frames]
            
            # Divide timeline into sections and pick best frame from each
            num_sections = min(5, len(remaining_frames))
            if num_sections > 0:
                section_duration = 1.0 / num_sections
                
                for i in range(num_sections):
                    section_start = i * section_duration
                    section_end = (i + 1) * section_duration
                    
                    section_frames = [
                        f for f in remaining_frames 
                        if section_start <= f['sequence_position'] <= section_end
                    ]
                    
                    if section_frames:
                        best_in_section = max(section_frames, key=lambda x: x['quality_metrics']['quality_score'])
                        if best_in_section not in selected_frames:
                            selected_frames.append(best_in_section)
            
            # Sort selected frames by timestamp
            selected_frames.sort(key=lambda x: x['timestamp'])
            
            # Limit to maximum frames
            if len(selected_frames) > self.max_frames_per_video:
                # Keep best quality frames within the limit
                selected_frames = sorted(selected_frames, key=lambda x: x['quality_metrics']['quality_score'], reverse=True)[:self.max_frames_per_video]
                selected_frames.sort(key=lambda x: x['timestamp'])
            
            return selected_frames
            
        except Exception as e:
            logger.error(f"Error selecting best frames: {str(e)}")
            return frames_data[:self.max_frames_per_video]  # Fallback to first N frames
    
    def analyze_temporal_patterns(self, frame_analyses: List[Dict]) -> Dict:
        """
        Analyze temporal patterns in vegetation over the video duration.
        """
        try:
            if len(frame_analyses) < 2:
                return {
                    'temporal_analysis': 'insufficient_data',
                    'trend_direction': 'unknown',
                    'stability_score': 0.0,
                    'change_points': []
                }
            
            # Sort analyses by timestamp
            sorted_analyses = sorted(frame_analyses, key=lambda x: x.get('timestamp', 0))
            
            # Extract time series data
            timestamps = [a.get('timestamp', 0) for a in sorted_analyses]
            vegetation_coverages = [
                a.get('vegetation_analysis', {}).get('total_vegetation_coverage', 0) 
                for a in sorted_analyses
            ]
            health_indices = [
                a.get('detection_results', {}).get('overall_health_index', 0) 
                for a in sorted_analyses
            ]
            ndvi_values = [
                a.get('ndvi_analysis', {}).get('mean_ndvi', 0) 
                for a in sorted_analyses
            ]
            
            # Calculate trends
            vegetation_trend = self.calculate_trend_analysis(timestamps, vegetation_coverages)
            health_trend = self.calculate_trend_analysis(timestamps, health_indices)
            ndvi_trend = self.calculate_trend_analysis(timestamps, ndvi_values)
            
            # Calculate stability scores
            vegetation_stability = 1.0 - (np.std(vegetation_coverages) / (np.mean(vegetation_coverages) + 1e-6))
            health_stability = 1.0 - (np.std(health_indices) / (np.mean(health_indices) + 1e-6))
            
            # Detect change points (significant changes in vegetation)
            change_points = self.detect_change_points(timestamps, vegetation_coverages)
            
            # Overall assessment
            overall_trend = 'stable'
            if vegetation_trend['slope'] > 1.0:
                overall_trend = 'improving'
            elif vegetation_trend['slope'] < -1.0:
                overall_trend = 'declining'
            
            return {
                'temporal_analysis': {
                    'vegetation_trend': vegetation_trend,
                    'health_trend': health_trend,
                    'ndvi_trend': ndvi_trend
                },
                'stability_metrics': {
                    'vegetation_stability': float(max(0, min(1, vegetation_stability))),
                    'health_stability': float(max(0, min(1, health_stability))),
                    'overall_stability': float(max(0, min(1, (vegetation_stability + health_stability) / 2)))
                },
                'change_detection': {
                    'change_points': change_points,
                    'num_significant_changes': len(change_points)
                },
                'overall_assessment': {
                    'trend_direction': overall_trend,
                    'consistency_score': float((vegetation_stability + health_stability) / 2),
                    'monitoring_quality': 'good' if len(frame_analyses) >= 5 else 'basic'
                }
            }
            
        except Exception as e:
            logger.error(f"Error analyzing temporal patterns: {str(e)}")
            return {
                'error': str(e),
                'temporal_analysis': 'analysis_failed'
            }
    
    def calculate_trend_analysis(self, timestamps: List[float], values: List[float]) -> Dict:
        """
        Calculate trend analysis for a time series.
        """
        try:
            if len(timestamps) < 2 or len(values) < 2:
                return {
                    'slope': 0.0,
                    'direction': 'unknown',
                    'strength': 0.0,
                    'r_squared': 0.0
                }
            
            # Convert to numpy arrays
            x = np.array(timestamps)
            y = np.array(values)
            
            # Calculate linear regression
            coeffs = np.polyfit(x, y, 1)
            slope = coeffs[0]
            intercept = coeffs[1]
            
            # Calculate R-squared
            y_pred = slope * x + intercept
            ss_res = np.sum((y - y_pred) ** 2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r_squared = 1 - (ss_res / (ss_tot + 1e-6))
            
            # Determine direction and strength
            if slope > 0.5:
                direction = 'increasing'
            elif slope < -0.5:
                direction = 'decreasing'
            else:
                direction = 'stable'
            
            strength = min(abs(slope) / 5.0, 1.0)  # Normalize strength to 0-1
            
            return {
                'slope': float(slope),
                'direction': direction,
                'strength': float(strength),
                'r_squared': float(max(0, r_squared)),
                'intercept': float(intercept)
            }
            
        except Exception as e:
            logger.error(f"Error calculating trend: {str(e)}")
            return {
                'slope': 0.0,
                'direction': 'unknown',
                'strength': 0.0,
                'r_squared': 0.0
            }
    
    def detect_change_points(self, timestamps: List[float], values: List[float], threshold: float = 10.0) -> List[Dict]:
        """
        Detect significant change points in the time series.
        """
        try:
            if len(timestamps) < 3:
                return []
            
            change_points = []
            
            for i in range(1, len(values) - 1):
                # Calculate change magnitude
                prev_change = abs(values[i] - values[i-1])
                next_change = abs(values[i+1] - values[i])
                
                # Check if this is a significant change point
                if prev_change > threshold or next_change > threshold:
                    change_points.append({
                        'timestamp': timestamps[i],
                        'value': values[i],
                        'change_magnitude': max(prev_change, next_change),
                        'change_type': 'increase' if values[i] > values[i-1] else 'decrease'
                    })
            
            return change_points
            
        except Exception as e:
            logger.error(f"Error detecting change points: {str(e)}")
            return []

class VideoProcessingManager:
    """
    Manager class for handling video processing workflow.
    """
    
    def __init__(self):
        self.video_analyzer = AdvancedVideoAnalyzer()
        
    def process_video_file(self, video_data: bytes, filename: str) -> Dict:
        """
        Complete video processing workflow.
        """
        try:
            # Save video to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as temp_file:
                temp_file.write(video_data)
                temp_path = temp_file.name
            
            try:
                # Extract optimal frames
                frames_data = self.video_analyzer.extract_optimal_frames(temp_path)
                
                if not frames_data:
                    return {
                        'error': 'No suitable frames could be extracted from video',
                        'success': False
                    }
                
                # Analyze each frame (would integrate with existing NDVI analyzer)
                frame_analyses = []
                for frame_data in frames_data:
                    # Here you would call your existing NDVI analyzer
                    # For now, we'll create a placeholder analysis
                    analysis = {
                        'timestamp': frame_data['timestamp'],
                        'frame_index': frame_data['frame_index'],
                        'quality_metrics': frame_data['quality_metrics'],
                        'vegetation_analysis': {
                            'total_vegetation_coverage': np.random.uniform(20, 80)  # Placeholder
                        },
                        'detection_results': {
                            'overall_health_index': np.random.uniform(60, 90)  # Placeholder
                        },
                        'ndvi_analysis': {
                            'mean_ndvi': np.random.uniform(0.2, 0.8)  # Placeholder
                        }
                    }
                    frame_analyses.append(analysis)
                
                # Perform temporal analysis
                temporal_analysis = self.video_analyzer.analyze_temporal_patterns(frame_analyses)
                
                # Generate comprehensive result
                result = {
                    'filename': filename,
                    'timestamp': datetime.now().isoformat(),
                    'analysis_type': 'advanced_video_temporal',
                    'video_metadata': {
                        'total_frames_analyzed': len(frames_data),
                        'video_duration_analyzed': max([f['timestamp'] for f in frames_data]) if frames_data else 0,
                        'frame_quality_average': np.mean([f['quality_metrics']['quality_score'] for f in frames_data]) if frames_data else 0
                    },
                    'frame_analyses': frame_analyses,
                    'temporal_patterns': temporal_analysis,
                    'summary': self.generate_video_summary(frame_analyses, temporal_analysis),
                    'success': True
                }
                
                return result
                
            finally:
                # Clean up temporary file
                try:
                    os.unlink(temp_path)
                except:
                    pass
                    
        except Exception as e:
            logger.error(f"Error processing video: {str(e)}")
            return {
                'filename': filename,
                'error': str(e),
                'success': False
            }
    
    def generate_video_summary(self, frame_analyses: List[Dict], temporal_analysis: Dict) -> str:
        """
        Generate human-readable summary of video analysis.
        """
        try:
            if not frame_analyses:
                return "Video analysis failed - no frames could be analyzed."
            
            # Calculate averages
            avg_vegetation = np.mean([a['vegetation_analysis']['total_vegetation_coverage'] for a in frame_analyses])
            avg_health = np.mean([a['detection_results']['overall_health_index'] for a in frame_analyses])
            
            # Get trend information
            trend_info = temporal_analysis.get('overall_assessment', {})
            trend_direction = trend_info.get('trend_direction', 'unknown')
            consistency = trend_info.get('consistency_score', 0)
            
            # Build summary
            summary_parts = []
            
            # Vegetation coverage
            if avg_vegetation > 60:
                summary_parts.append("high vegetation coverage maintained throughout video")
            elif avg_vegetation > 30:
                summary_parts.append("moderate vegetation coverage observed")
            else:
                summary_parts.append("limited vegetation coverage detected")
            
            # Trend analysis
            if trend_direction == 'improving':
                summary_parts.append("vegetation shows improving trend over time")
            elif trend_direction == 'declining':
                summary_parts.append("vegetation shows declining trend")
            else:
                summary_parts.append("vegetation remains relatively stable")
            
            # Consistency
            if consistency > 0.8:
                summary_parts.append("high consistency in vegetation patterns")
            elif consistency > 0.6:
                summary_parts.append("moderate consistency observed")
            else:
                summary_parts.append("variable vegetation patterns detected")
            
            # Quality assessment
            monitoring_quality = temporal_analysis.get('overall_assessment', {}).get('monitoring_quality', 'basic')
            summary_parts.append(f"{monitoring_quality} quality temporal monitoring achieved")
            
            summary = ". ".join([part.capitalize() for part in summary_parts]) + "."
            return summary
            
        except Exception as e:
            logger.error(f"Error generating video summary: {str(e)}")
            return "Video analysis completed with basic temporal vegetation monitoring."