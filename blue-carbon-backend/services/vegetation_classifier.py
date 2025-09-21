import cv2
import numpy as np
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import joblib
import os
from typing import Dict, List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)

class VegetationClassifier:
    """
    Advanced vegetation classification using machine learning and computer vision.
    Detects planted vs empty land with high accuracy.
    """
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.classifier = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            class_weight='balanced'
        )
        self.is_trained = False
        self.feature_names = [
            'mean_red', 'mean_green', 'mean_blue',
            'std_red', 'std_green', 'std_blue',
            'green_red_ratio', 'green_blue_ratio',
            'vegetation_index', 'texture_contrast',
            'edge_density', 'color_diversity'
        ]
    
    def extract_color_features(self, image_patch: np.ndarray) -> np.ndarray:
        """
        Extract comprehensive color-based features from image patch.
        """
        try:
            # Basic color statistics
            mean_red = np.mean(image_patch[:, :, 0])
            mean_green = np.mean(image_patch[:, :, 1])
            mean_blue = np.mean(image_patch[:, :, 2])
            
            std_red = np.std(image_patch[:, :, 0])
            std_green = np.std(image_patch[:, :, 1])
            std_blue = np.std(image_patch[:, :, 2])
            
            # Color ratios (vegetation indicators)
            green_red_ratio = mean_green / (mean_red + 1e-6)
            green_blue_ratio = mean_green / (mean_blue + 1e-6)
            
            # Simple vegetation index
            vegetation_index = (mean_green - mean_red) / (mean_green + mean_red + 1e-6)
            
            return np.array([
                mean_red, mean_green, mean_blue,
                std_red, std_green, std_blue,
                green_red_ratio, green_blue_ratio,
                vegetation_index
            ])
            
        except Exception as e:
            logger.error(f"Error extracting color features: {str(e)}")
            return np.zeros(9)
    
    def extract_texture_features(self, image_patch: np.ndarray) -> np.ndarray:
        """
        Extract texture-based features for vegetation detection.
        """
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(image_patch, cv2.COLOR_RGB2GRAY)
            
            # Calculate texture contrast using local variance
            kernel = np.ones((5, 5), np.float32) / 25
            local_mean = cv2.filter2D(gray.astype(np.float32), -1, kernel)
            local_variance = cv2.filter2D((gray.astype(np.float32) - local_mean) ** 2, -1, kernel)
            texture_contrast = np.mean(local_variance)
            
            # Edge density using Canny edge detection
            edges = cv2.Canny(gray, 50, 150)
            edge_density = np.sum(edges > 0) / edges.size
            
            return np.array([texture_contrast, edge_density])
            
        except Exception as e:
            logger.error(f"Error extracting texture features: {str(e)}")
            return np.zeros(2)
    
    def extract_diversity_features(self, image_patch: np.ndarray) -> np.ndarray:
        """
        Extract color diversity features using k-means clustering.
        """
        try:
            # Reshape image for k-means
            pixels = image_patch.reshape(-1, 3)
            
            # Perform k-means clustering to find dominant colors
            n_colors = min(5, len(pixels))  # Max 5 color clusters
            if n_colors > 1:
                kmeans = KMeans(n_clusters=n_colors, random_state=42, n_init=10)
                kmeans.fit(pixels)
                
                # Calculate color diversity (variance in cluster centers)
                centers = kmeans.cluster_centers_
                color_diversity = np.var(centers.flatten())
            else:
                color_diversity = 0.0
            
            return np.array([color_diversity])
            
        except Exception as e:
            logger.error(f"Error extracting diversity features: {str(e)}")
            return np.zeros(1)
    
    def extract_all_features(self, image_patch: np.ndarray) -> np.ndarray:
        """
        Extract all features from an image patch.
        """
        try:
            color_features = self.extract_color_features(image_patch)
            texture_features = self.extract_texture_features(image_patch)
            diversity_features = self.extract_diversity_features(image_patch)
            
            # Combine all features
            all_features = np.concatenate([color_features, texture_features, diversity_features])
            return all_features
            
        except Exception as e:
            logger.error(f"Error extracting features: {str(e)}")
            return np.zeros(len(self.feature_names))
    
    def create_training_data(self, image: np.ndarray, vegetation_mask: np.ndarray, 
                           patch_size: int = 32) -> Tuple[np.ndarray, np.ndarray]:
        """
        Create training data from image and vegetation mask.
        """
        try:
            features = []
            labels = []
            
            height, width = image.shape[:2]
            step = patch_size // 2  # Overlapping patches
            
            for y in range(0, height - patch_size, step):
                for x in range(0, width - patch_size, step):
                    # Extract patch
                    patch = image[y:y+patch_size, x:x+patch_size]
                    mask_patch = vegetation_mask[y:y+patch_size, x:x+patch_size]
                    
                    # Skip patches that are too small
                    if patch.shape[0] < patch_size or patch.shape[1] < patch_size:
                        continue
                    
                    # Extract features
                    patch_features = self.extract_all_features(patch)
                    
                    # Determine label (vegetation if >50% of patch is vegetation)
                    vegetation_ratio = np.sum(mask_patch) / (patch_size * patch_size)
                    label = 1 if vegetation_ratio > 0.5 else 0
                    
                    features.append(patch_features)
                    labels.append(label)
            
            return np.array(features), np.array(labels)
            
        except Exception as e:
            logger.error(f"Error creating training data: {str(e)}")
            return np.array([]), np.array([])
    
    def train_classifier(self, images: List[np.ndarray], vegetation_masks: List[np.ndarray]):
        """
        Train the vegetation classifier on provided data.
        """
        try:
            all_features = []
            all_labels = []
            
            # Extract features from all training images
            for image, mask in zip(images, vegetation_masks):
                features, labels = self.create_training_data(image, mask)
                if len(features) > 0:
                    all_features.append(features)
                    all_labels.append(labels)
            
            if not all_features:
                logger.error("No training data could be extracted")
                return False
            
            # Combine all training data
            X = np.vstack(all_features)
            y = np.hstack(all_labels)
            
            # Scale features
            X_scaled = self.scaler.fit_transform(X)
            
            # Train classifier
            self.classifier.fit(X_scaled, y)
            self.is_trained = True
            
            # Log training results
            accuracy = self.classifier.score(X_scaled, y)
            logger.info(f"Classifier trained with {len(X)} samples, accuracy: {accuracy:.3f}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error training classifier: {str(e)}")
            return False
    
    def classify_vegetation(self, image: np.ndarray, patch_size: int = 32) -> Dict:
        """
        Classify vegetation in the entire image using trained model.
        """
        try:
            if not self.is_trained:
                # Use rule-based classification if no trained model
                return self.rule_based_classification(image)
            
            height, width = image.shape[:2]
            vegetation_probability = np.zeros((height, width))
            coverage_map = np.zeros((height, width))
            
            step = patch_size // 4  # High overlap for smooth results
            
            for y in range(0, height - patch_size + 1, step):
                for x in range(0, width - patch_size + 1, step):
                    # Extract patch
                    patch = image[y:y+patch_size, x:x+patch_size]
                    
                    # Extract features
                    patch_features = self.extract_all_features(patch).reshape(1, -1)
                    
                    # Scale features
                    patch_features_scaled = self.scaler.transform(patch_features)
                    
                    # Predict vegetation probability
                    prob = self.classifier.predict_proba(patch_features_scaled)[0, 1]
                    
                    # Update probability map
                    vegetation_probability[y:y+patch_size, x:x+patch_size] += prob
                    coverage_map[y:y+patch_size, x:x+patch_size] += 1
            
            # Normalize by coverage
            coverage_map = np.maximum(coverage_map, 1)  # Avoid division by zero
            vegetation_probability = vegetation_probability / coverage_map
            
            # Create binary vegetation mask
            vegetation_mask = vegetation_probability > 0.5
            
            # Calculate statistics
            total_pixels = height * width
            vegetation_pixels = np.sum(vegetation_mask)
            vegetation_percentage = (vegetation_pixels / total_pixels) * 100
            
            # Analyze planted vs empty areas
            planted_analysis = self.analyze_planted_areas(image, vegetation_mask, vegetation_probability)
            
            return {
                'vegetation_mask': vegetation_mask,
                'vegetation_probability': vegetation_probability,
                'vegetation_percentage': vegetation_percentage,
                'planted_analysis': planted_analysis,
                'classification_method': 'machine_learning'
            }
            
        except Exception as e:
            logger.error(f"Error classifying vegetation: {str(e)}")
            return self.rule_based_classification(image)
    
    def rule_based_classification(self, image: np.ndarray) -> Dict:
        """
        Fallback rule-based vegetation classification.
        """
        try:
            # Convert to HSV for better vegetation detection
            hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
            
            # Define vegetation color ranges in HSV
            # Green vegetation range
            lower_green = np.array([35, 30, 20])
            upper_green = np.array([85, 255, 255])
            
            green_mask = cv2.inRange(hsv, lower_green, upper_green)
            
            # Additional vegetation detection using color ratios
            green_channel = image[:, :, 1].astype(np.float32)
            red_channel = image[:, :, 0].astype(np.float32)
            blue_channel = image[:, :, 2].astype(np.float32)
            
            # Vegetation index mask
            vegetation_index = (green_channel - red_channel) / (green_channel + red_channel + 1e-6)
            vegetation_index_mask = vegetation_index > 0.1
            
            # Combine masks
            vegetation_mask = (green_mask > 0) | vegetation_index_mask
            
            # Calculate statistics
            total_pixels = image.shape[0] * image.shape[1]
            vegetation_pixels = np.sum(vegetation_mask)
            vegetation_percentage = (vegetation_pixels / total_pixels) * 100
            
            # Create probability map (simple binary to probability conversion)
            vegetation_probability = vegetation_mask.astype(np.float32)
            
            # Analyze planted areas
            planted_analysis = self.analyze_planted_areas(image, vegetation_mask, vegetation_probability)
            
            return {
                'vegetation_mask': vegetation_mask,
                'vegetation_probability': vegetation_probability,
                'vegetation_percentage': vegetation_percentage,
                'planted_analysis': planted_analysis,
                'classification_method': 'rule_based'
            }
            
        except Exception as e:
            logger.error(f"Error in rule-based classification: {str(e)}")
            return {
                'vegetation_mask': np.zeros((image.shape[0], image.shape[1]), dtype=bool),
                'vegetation_probability': np.zeros((image.shape[0], image.shape[1])),
                'vegetation_percentage': 0.0,
                'planted_analysis': {},
                'classification_method': 'error_fallback'
            }
    
    def analyze_planted_areas(self, image: np.ndarray, vegetation_mask: np.ndarray, 
                            vegetation_probability: np.ndarray) -> Dict:
        """
        Analyze planted vs empty areas with detailed metrics.
        """
        try:
            # Convert to different color spaces for analysis
            hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
            lab = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
            
            # Detect bare soil/sand areas
            hue = hsv[:, :, 0]
            saturation = hsv[:, :, 1]
            value = hsv[:, :, 2]
            
            # Soil detection (brown/tan colors)
            soil_mask = ((10 <= hue) & (hue <= 30)) & (saturation > 15) & (value > 30)
            
            # Sand detection (light colors with low saturation)
            sand_mask = (saturation < 30) & (value > 150)
            
            # Water detection (blue colors)
            water_mask = ((100 <= hue) & (hue <= 130)) & (saturation > 50) & (value > 50)
            
            # Rock/concrete detection (gray areas)
            rock_mask = (saturation < 20) & (value < 150) & (value > 50)
            
            # Calculate area percentages
            total_pixels = image.shape[0] * image.shape[1]
            
            planted_area = np.sum(vegetation_mask) / total_pixels * 100
            soil_area = np.sum(soil_mask) / total_pixels * 100
            sand_area = np.sum(sand_mask) / total_pixels * 100
            water_area = np.sum(water_mask) / total_pixels * 100
            rock_area = np.sum(rock_mask) / total_pixels * 100
            
            # Calculate empty land (soil + sand + rock, excluding water)
            empty_land = soil_area + sand_area + rock_area
            
            # Vegetation density analysis
            high_density_vegetation = vegetation_probability > 0.8
            medium_density_vegetation = (vegetation_probability > 0.5) & (vegetation_probability <= 0.8)
            low_density_vegetation = (vegetation_probability > 0.2) & (vegetation_probability <= 0.5)
            
            high_density_percentage = np.sum(high_density_vegetation) / total_pixels * 100
            medium_density_percentage = np.sum(medium_density_vegetation) / total_pixels * 100
            low_density_percentage = np.sum(low_density_vegetation) / total_pixels * 100
            
            # Spatial distribution analysis
            vegetation_clusters = self.analyze_vegetation_clusters(vegetation_mask)
            
            return {
                'land_composition': {
                    'planted_area_percentage': planted_area,
                    'empty_land_percentage': empty_land,
                    'soil_percentage': soil_area,
                    'sand_percentage': sand_area,
                    'water_percentage': water_area,
                    'rock_concrete_percentage': rock_area
                },
                'vegetation_density': {
                    'high_density_percentage': high_density_percentage,
                    'medium_density_percentage': medium_density_percentage,
                    'low_density_percentage': low_density_percentage
                },
                'spatial_analysis': vegetation_clusters,
                'planting_assessment': {
                    'likely_planted': planted_area > 20 and high_density_percentage > 5,
                    'planting_quality': 'high' if high_density_percentage > 15 
                                     else 'medium' if medium_density_percentage > 20 
                                     else 'low',
                    'coverage_uniformity': 1.0 - (np.std(vegetation_probability) / (np.mean(vegetation_probability) + 1e-6))
                }
            }
            
        except Exception as e:
            logger.error(f"Error analyzing planted areas: {str(e)}")
            return {}
    
    def analyze_vegetation_clusters(self, vegetation_mask: np.ndarray) -> Dict:
        """
        Analyze spatial distribution of vegetation using connected components.
        """
        try:
            # Find connected components
            num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(
                vegetation_mask.astype(np.uint8), connectivity=8
            )
            
            # Exclude background (label 0)
            if num_labels > 1:
                cluster_sizes = stats[1:, cv2.CC_STAT_AREA]  # Areas of clusters
                cluster_count = len(cluster_sizes)
                
                # Calculate cluster statistics
                avg_cluster_size = np.mean(cluster_sizes)
                largest_cluster_size = np.max(cluster_sizes)
                cluster_size_variance = np.var(cluster_sizes)
                
                # Classify distribution pattern
                if cluster_count == 1:
                    distribution_pattern = "single_large_area"
                elif cluster_count <= 5 and avg_cluster_size > 1000:
                    distribution_pattern = "few_large_clusters"
                elif cluster_count > 20 and avg_cluster_size < 100:
                    distribution_pattern = "many_small_patches"
                else:
                    distribution_pattern = "mixed_distribution"
                
                return {
                    'cluster_count': int(cluster_count),
                    'average_cluster_size': float(avg_cluster_size),
                    'largest_cluster_size': float(largest_cluster_size),
                    'cluster_size_variance': float(cluster_size_variance),
                    'distribution_pattern': distribution_pattern
                }
            else:
                return {
                    'cluster_count': 0,
                    'average_cluster_size': 0.0,
                    'largest_cluster_size': 0.0,
                    'cluster_size_variance': 0.0,
                    'distribution_pattern': "no_vegetation"
                }
                
        except Exception as e:
            logger.error(f"Error analyzing vegetation clusters: {str(e)}")
            return {}
    
    def save_model(self, filepath: str):
        """
        Save the trained model to file.
        """
        try:
            if self.is_trained:
                model_data = {
                    'classifier': self.classifier,
                    'scaler': self.scaler,
                    'feature_names': self.feature_names,
                    'is_trained': self.is_trained
                }
                joblib.dump(model_data, filepath)
                logger.info(f"Model saved to {filepath}")
                return True
            else:
                logger.warning("No trained model to save")
                return False
                
        except Exception as e:
            logger.error(f"Error saving model: {str(e)}")
            return False
    
    def load_model(self, filepath: str):
        """
        Load a trained model from file.
        """
        try:
            if os.path.exists(filepath):
                model_data = joblib.load(filepath)
                self.classifier = model_data['classifier']
                self.scaler = model_data['scaler']
                self.feature_names = model_data['feature_names']
                self.is_trained = model_data['is_trained']
                logger.info(f"Model loaded from {filepath}")
                return True
            else:
                logger.warning(f"Model file not found: {filepath}")
                return False
                
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            return False