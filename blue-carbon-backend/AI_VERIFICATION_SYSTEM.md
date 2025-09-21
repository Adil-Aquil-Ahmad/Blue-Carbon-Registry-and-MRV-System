# AI-Based Dynamic Carbon Credit Calculation System

## Overview

This enhanced blue carbon registry system now uses AI-powered image analysis to dynamically calculate carbon credits based on actual vegetation transformation and CO₂ sequestration potential, replacing the previous fixed 100-credit system.

## Key Features

### 🌱 Before/After Image Analysis
- Upload paired before and after images to document land transformation
- AI analyzes vegetation coverage, NDVI improvements, and land use changes
- Detects transitions from barren land to green vegetation (key metric for restoration projects)

### 🧠 Dynamic Credit Calculation
- Credits calculated based on actual CO₂ sequestration potential
- Considers project area in hectares
- Applies ecosystem-specific multipliers (mangrove, seagrass, salt marsh, etc.)
- Includes quality bonuses for exceptional transformations

### 📊 Comprehensive Analysis
- NDVI (Normalized Difference Vegetation Index) analysis
- Vegetation health assessment
- Land use change classification
- Confidence scoring and verification levels

## How It Works

### 1. Evidence Upload
```http
POST /upload
```

**Required Fields for AI Analysis:**
- `evidence_type`: Must be "before" or "after"
- `project_area_hectares`: Project size in hectares
- `files`: Image file(s) showing the project area

**Example:**
```bash
curl -X POST "http://localhost:8000/upload" \
  -F "project_id=1" \
  -F "uploader=user@example.com" \
  -F "gps=9.0579,76.2711" \
  -F "co2=150" \
  -F "evidence_type=before" \
  -F "project_area_hectares=5.5" \
  -F "files=@before_image.jpg"
```

### 2. Automatic AI Analysis
When both before and after images are uploaded for a project:
- System automatically triggers AI comparison analysis
- Calculates vegetation transformation metrics
- Determines CO₂ sequestration potential
- Recommends carbon credits based on scientific models

### 3. Verification with Dynamic Credits
```http
POST /verify
```

The verification process now:
- Uses AI-calculated credits when available
- Falls back to manual override if specified
- Includes comprehensive analysis report
- Provides transparency on calculation methods

## Credit Calculation Formula

### Base Calculation
```
Base Credits = CO₂ Sequestration (kg) × Credit Conversion Rate (0.1)
```

### CO₂ Sequestration Calculation
```
CO₂ Sequestration = Base Rate × Transformation Multiplier × NDVI Multiplier × Area Factor × Hectares × Years
```

**Base Rates (kg CO₂/ha/year):**
- Mangrove: 1,500
- Salt Marsh: 1,200
- Seagrass: 830
- Coastal Wetland: 900
- Restored Vegetation: 600

**Transformation Multipliers:**
- Barren to Dense Vegetation: 2.5x
- Barren to Moderate Vegetation: 1.8x
- Sparse to Dense Vegetation: 1.5x
- Maintained Vegetation: 1.0x

**NDVI Improvement Multipliers:**
- NDVI improvement > 0.4: 2.0x
- NDVI improvement > 0.3: 1.7x
- NDVI improvement > 0.2: 1.4x
- NDVI improvement > 0.1: 1.1x

### Quality Adjustments
- **Transformation Quality:** Excellent (1.3x), Very Good (1.2x), Good (1.1x)
- **Verification Confidence:** High confidence bonus (1.1x), Low confidence penalty
- **Project Bonuses:** Restoration projects, large scale, exceptional transformation

## New API Endpoints

### Evidence Analysis
```http
GET /evidences/{evidence_id}/analysis
```
Get detailed AI analysis results for specific evidence.

### Project Credit Calculation
```http
GET /projects/{project_id}/credit-calculation
```
Get comprehensive credit calculation details for a project.

### Manual Analysis Trigger
```http
POST /projects/{project_id}/trigger-analysis?project_area_hectares=5.5
```
Manually trigger AI analysis for projects with before/after evidence.

### System Statistics
```http
GET /system/ai-verification-stats
```
Get system-wide AI verification adoption and performance statistics.

## Database Schema Updates

### Enhanced MRVData Table
New fields added to support AI verification:

```sql
-- Evidence Classification
evidence_type TEXT DEFAULT 'general'  -- 'before', 'after', 'general'
before_image_hash TEXT
after_image_hash TEXT
project_area_hectares REAL

-- AI Analysis Results
calculated_co2_sequestration REAL
vegetation_change_percentage REAL
ndvi_improvement REAL
land_transformation_score REAL

-- Dynamic Credits
calculated_carbon_credits REAL
credit_calculation_method TEXT DEFAULT 'ai_analysis'

-- Analysis Metadata
ai_analysis_results TEXT  -- JSON blob with full analysis
confidence_score REAL
analysis_summary TEXT
```

## Migration Guide

### 1. Update Database Schema
```bash
cd blue-carbon-backend
python migrate_database.py
```

### 2. Test the System
```bash
python test_ai_verification.py
```

### 3. Upload Before/After Images
Use the new upload endpoint with `evidence_type` field:
- Upload "before" image first
- Upload "after" image second
- System will automatically trigger AI analysis

## Verification Levels

### High Confidence (≥85%)
- **Action:** Approve full credits
- **Characteristics:** Clear transformation, high NDVI improvement, good image quality

### Good Confidence (70-84%)
- **Action:** Approve with monitoring
- **Characteristics:** Solid transformation evidence, acceptable image quality

### Moderate Confidence (55-69%)
- **Action:** Approve partial credits
- **Characteristics:** Some transformation visible, moderate confidence in analysis

### Low Confidence (40-54%)
- **Action:** Require additional evidence
- **Characteristics:** Unclear transformation, poor image quality

### Insufficient (<40%)
- **Action:** Require manual review
- **Characteristics:** No clear transformation, analysis unreliable

## Best Practices

### Image Requirements
- **Resolution:** Minimum 800x600 pixels
- **Format:** JPG, PNG, or similar
- **Coverage:** Show the entire project area
- **Timing:** Before image should show initial state, after image should show transformation
- **Consistency:** Use similar angles and lighting conditions

### Project Setup
- **Area Measurement:** Accurately measure project area in hectares
- **Documentation:** Maintain clear records of project timeline
- **Monitoring:** Regular monitoring recommended for ongoing projects

## Troubleshooting

### Common Issues

1. **No AI Analysis Triggered**
   - Ensure both before and after images are uploaded
   - Verify `project_area_hectares` is provided
   - Check that `evidence_type` is set correctly

2. **Low Confidence Scores**
   - Improve image quality
   - Ensure consistent imaging conditions
   - Verify project area measurements

3. **Unexpected Credit Amounts**
   - Review project area (major factor in calculation)
   - Check vegetation transformation quality
   - Verify ecosystem type detection

### Debug Endpoints

**Get Analysis Details:**
```http
GET /evidences/{evidence_id}/analysis
```

**System Health Check:**
```http
GET /system/ai-verification-stats
```

## Example Workflow

### Complete Project Verification

1. **Initial Upload (Before Image)**
```bash
curl -X POST "http://localhost:8000/upload" \
  -F "project_id=1" \
  -F "evidence_type=before" \
  -F "project_area_hectares=10.0" \
  -F "files=@project_before.jpg"
```

2. **Progress Upload (After Image)**
```bash
curl -X POST "http://localhost:8000/upload" \
  -F "project_id=1" \
  -F "evidence_type=after" \
  -F "project_area_hectares=10.0" \
  -F "files=@project_after.jpg"
```

3. **Check Analysis Results**
```bash
curl "http://localhost:8000/projects/1/credit-calculation"
```

4. **Verify and Issue Credits**
```bash
curl -X POST "http://localhost:8000/verify" \
  -H "Content-Type: application/json" \
  -d '{"evidence_id": 123, "mint_receipt": false}'
```

## Scientific Basis

The credit calculation is based on:
- **IPCC Guidelines** for blue carbon ecosystems
- **Peer-reviewed research** on coastal ecosystem sequestration rates
- **Remote sensing** vegetation analysis techniques
- **Conservation biology** restoration success metrics

### Key References
- Coastal Blue Carbon: Methods for assessing carbon stocks and emissions factors
- NDVI-based vegetation monitoring in coastal restoration projects
- CO₂ sequestration rates in mangrove, seagrass, and salt marsh ecosystems

## Support and Maintenance

### Monitoring
- Use `/system/ai-verification-stats` to monitor adoption
- Track confidence scores and calculation methods
- Review verification success rates

### Updates
- AI models can be improved with additional training data
- Sequestration rates can be updated based on new research
- Credit conversion rates can be adjusted for policy changes

---

**Note:** This system provides AI-assisted credit calculation but should be used alongside expert review for high-value projects. The AI analysis enhances transparency and consistency but doesn't replace human expertise in conservation project evaluation.