from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import io
import logging
from typing import List, Dict, Optional
import asyncio
from datetime import datetime
import uuid
import os

# Import our AI services
from services.ai_verification import NDVIAnalyzer, VideoAnalyzer
from services.vegetation_classifier import VegetationClassifier
from services.project_verification_integration import ProjectVerificationIntegration

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create router
ai_router = APIRouter(prefix="/api/ai-verification", tags=["AI Verification"])

# Initialize AI services
ndvi_analyzer = NDVIAnalyzer()
video_analyzer = VideoAnalyzer()
vegetation_classifier = VegetationClassifier()

# Supported file types
SUPPORTED_IMAGE_TYPES = {
    'image/jpeg', 'image/jpg', 'image/png', 'image/tiff', 'image/tif', 'image/bmp'
}
SUPPORTED_VIDEO_TYPES = {
    'video/mp4', 'video/avi', 'video/mov', 'video/mkv', 'video/wmv'
}

# In-memory storage for demo purposes
analysis_results = {}

@ai_router.post("/analyze-image")
async def analyze_image(
    file: UploadFile = File(...),
    project_id: Optional[int] = None
):
    """
    Analyze uploaded image for vegetation and mangrove detection.
    """
    try:
        # Validate file type
        if file.content_type not in SUPPORTED_IMAGE_TYPES:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type. Supported types: {', '.join(SUPPORTED_IMAGE_TYPES)}"
            )
        
        # Read file content
        contents = await file.read()
        
        # Generate analysis ID
        analysis_id = str(uuid.uuid4())
        
        # Create file-like object for processing
        image_stream = io.BytesIO(contents)
        
        # Perform NDVI analysis
        logger.info(f"Starting NDVI analysis for {file.filename}")
        ndvi_result = await asyncio.to_thread(ndvi_analyzer.analyze_image, image_stream)
        
        # Reset stream for vegetation classification
        image_stream.seek(0)
        
        # Perform vegetation classification
        logger.info(f"Starting vegetation classification for {file.filename}")
        vegetation_result = await asyncio.to_thread(vegetation_classifier.classify_vegetation, image_stream)
        
        # Combine results
        combined_result = {
            "analysis_id": analysis_id,
            "filename": file.filename,
            "file_size": len(contents),
            "timestamp": datetime.now().isoformat(),
            "ndvi_analysis": ndvi_result,
            "vegetation_classification": vegetation_result,
            "overall_score": (ndvi_result.get("overall_score", 0) + vegetation_result.get("confidence", 0)) / 2,
            "project_id": project_id
        }
        
        # Store result in memory
        analysis_results[analysis_id] = combined_result
        
        # Link to project if provided
        if project_id:
            ProjectVerificationIntegration.link_verification_to_project(
                project_id, analysis_id, "image_analysis"
            )
        
        logger.info(f"Analysis completed for {file.filename}: {analysis_id}")
        
        return JSONResponse(content={
            "status": "success",
            "message": "Image analysis completed successfully",
            "data": combined_result
        })
        
    except Exception as e:
        logger.error(f"Error analyzing image {file.filename}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@ai_router.post("/analyze-video")
async def analyze_video(
    file: UploadFile = File(...),
    project_id: Optional[int] = None
):
    """
    Analyze uploaded video for temporal vegetation monitoring.
    """
    try:
        # Validate file type
        if file.content_type not in SUPPORTED_VIDEO_TYPES:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type. Supported types: {', '.join(SUPPORTED_VIDEO_TYPES)}"
            )
        
        # Read file content
        contents = await file.read()
        
        # Generate analysis ID
        analysis_id = str(uuid.uuid4())
        
        # Create temporary file for video processing
        temp_filename = f"temp_{analysis_id}.mp4"
        with open(temp_filename, "wb") as temp_file:
            temp_file.write(contents)
        
        try:
            # Perform video analysis
            logger.info(f"Starting video analysis for {file.filename}")
            video_result = await asyncio.to_thread(video_analyzer.analyze_video, temp_filename)
            
            # Combine results
            combined_result = {
                "analysis_id": analysis_id,
                "filename": file.filename,
                "file_size": len(contents),
                "timestamp": datetime.now().isoformat(),
                "video_analysis": video_result,
                "overall_score": video_result.get("average_ndvi", 0) * 100,
                "project_id": project_id
            }
            
            # Store result in memory
            analysis_results[analysis_id] = combined_result
            
            # Link to project if provided
            if project_id:
                ProjectVerificationIntegration.link_verification_to_project(
                    project_id, analysis_id, "video_analysis"
                )
            
            logger.info(f"Video analysis completed for {file.filename}: {analysis_id}")
            
            return JSONResponse(content={
                "status": "success",
                "message": "Video analysis completed successfully",
                "data": combined_result
            })
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_filename):
                os.remove(temp_filename)
        
    except Exception as e:
        logger.error(f"Error analyzing video {file.filename}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Video analysis failed: {str(e)}")

@ai_router.get("/analysis-history")
async def get_analysis_history(limit: int = 10):
    """
    Get recent analysis history.
    """
    try:
        # Return recent results from memory storage
        recent_results = list(analysis_results.values())[-limit:]
        
        return JSONResponse(content={
            "status": "success",
            "data": recent_results,
            "total": len(analysis_results)
        })
        
    except Exception as e:
        logger.error(f"Error retrieving analysis history: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve history: {str(e)}")

@ai_router.get("/analysis/{analysis_id}")
async def get_analysis_result(analysis_id: str):
    """
    Get specific analysis result by ID.
    """
    try:
        if analysis_id not in analysis_results:
            raise HTTPException(status_code=404, detail="Analysis result not found")
        
        result = analysis_results[analysis_id]
        
        return JSONResponse(content={
            "status": "success",
            "data": result
        })
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving analysis {analysis_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve analysis: {str(e)}")

@ai_router.get("/project/{project_id}/verification-score")
async def get_project_verification_score(project_id: int):
    """
    Get overall verification score for a project.
    """
    try:
        score = ProjectVerificationIntegration.calculate_project_verification_score(project_id)
        
        return JSONResponse(content={
            "status": "success",
            "data": score
        })
        
    except Exception as e:
        logger.error(f"Error calculating project verification score: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to calculate score: {str(e)}")

@ai_router.get("/project/{project_id}/compliance-report")
async def get_compliance_report(project_id: int):
    """
    Generate compliance report for a project.
    """
    try:
        report = ProjectVerificationIntegration.generate_compliance_report(project_id)
        
        return JSONResponse(content={
            "status": "success",
            "data": report
        })
        
    except Exception as e:
        logger.error(f"Error generating compliance report: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate report: {str(e)}")

@ai_router.get("/health")
async def health_check():
    """
    Health check endpoint for AI verification service.
    """
    return JSONResponse(content={
        "status": "healthy",
        "service": "AI Verification",
        "timestamp": datetime.now().isoformat(),
        "features": {
            "image_analysis": True,
            "video_analysis": True,
            "vegetation_classification": True,
            "ndvi_calculation": True
        }
    })