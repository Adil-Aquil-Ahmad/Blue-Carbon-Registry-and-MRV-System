from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON, Float, Text
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

# Import auth models to ensure they use the same Base
from .auth_model import User, LoginSession, UserRole

class MRVData(Base):
    __tablename__ = "mrvdata"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, index=True)
    uploader = Column(String)
    gps = Column(String)
    co2 = Column(String)  # Legacy field - will be replaced by calculated_co2_sequestration
    media_hashes = Column(JSON)
    evidence_hash = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    verified = Column(Boolean, default=False)
    
    # New fields for before/after image analysis
    evidence_type = Column(String, default='general')  # 'before', 'after', 'general'
    before_image_hash = Column(String)  # Hash of before image
    after_image_hash = Column(String)   # Hash of after image
    project_area_hectares = Column(Float)  # Area of the project in hectares
    
    # AI Analysis Results
    calculated_co2_sequestration = Column(Float)  # Calculated CO2 sequestration in kg
    vegetation_change_percentage = Column(Float)  # % change in vegetation coverage
    ndvi_improvement = Column(Float)  # NDVI improvement score
    land_transformation_score = Column(Float)  # Score indicating barren->green transformation
    
    # Dynamic Carbon Credits
    calculated_carbon_credits = Column(Float)  # Dynamically calculated carbon credits
    credit_calculation_method = Column(String, default='ai_analysis')  # 'fixed', 'ai_analysis'
    
    # Green Progress Analysis
    green_progress_multiplier = Column(Float, default=1.0)  # Greenness-based multiplier (0-1.5)
    green_progress_level = Column(String)  # 'Exceptional', 'Significant', 'Good', etc.
    before_green_percentage = Column(Float)  # % of green pixels in before image
    after_green_percentage = Column(Float)   # % of green pixels in after image
    green_improvement = Column(Float)        # Difference in green percentage
    
    # AI Analysis Metadata
    ai_analysis_results = Column(JSON)  # Complete AI analysis results
    confidence_score = Column(Float)  # AI analysis confidence score
    analysis_summary = Column(Text)  # Human-readable analysis summary

class ProjectData(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    blockchain_id = Column(Integer, index=True)  # ID from blockchain
    name = Column(String, index=True)
    location = Column(String)
    hectares = Column(Integer)
    owner = Column(String, index=True)  # Wallet address
    project_metadata = Column(String)  # Renamed from 'metadata' to avoid SQLAlchemy conflict
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    tx_hash = Column(String)  # Blockchain transaction hash
    verified_on_blockchain = Column(Boolean, default=False)
    total_issued_credits = Column(Float, default=0.0)
