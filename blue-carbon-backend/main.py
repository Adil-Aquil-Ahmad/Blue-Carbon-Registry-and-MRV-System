# main.py
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Any, Optional, Dict
from hexbytes import HexBytes
from web3 import Web3
import json
import os
import hashlib
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ⬇️ DB + MRV integration
from database import SessionLocal
from models.db_model import MRVData
from models.auth_model import User, UserRole
from services.mrv import upload_field_data
from services.auth import AuthService

# AI Verification Services (temporarily disabled)
from services.ai_endpoints import ai_router
from services.dynamic_carbon_credit_calculator import DynamicCarbonCreditCalculator
# from services.admin import admin_router
# from services.blockchain import blockchain_router

app = FastAPI()

# ---------------- CORS Setup ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- Blockchain Setup ----------------
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
if not w3.is_connected():
    print("⚠️ Warning: web3 not connected to http://127.0.0.1:8545")

REGISTRY_ADDRESS = os.getenv("REGISTRY_ADDRESS", "0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512")
TOKEN_ADDRESS = os.getenv("TOKEN_ADDRESS", "0x5FbDB2315678afecb367f032d93F642f64180aa3")

# Use relative paths to the local contract files
REGISTRY_ABI_PATH = os.path.join(os.path.dirname(__file__), "contracts", "BlueCarbonRegistry.json")
TOKEN_ABI_PATH = os.path.join(os.path.dirname(__file__), "..", "blue-carbon-contracts", "artifacts", "contracts", "BlueCarbonRegistry.sol", "CarbonToken.json")

with open(REGISTRY_ABI_PATH, "r", encoding="utf-8") as f:
    registry_abi = json.load(f)["abi"]
with open(TOKEN_ABI_PATH, "r", encoding="utf-8") as f:
    token_abi = json.load(f)["abi"]

registry = w3.eth.contract(address=Web3.to_checksum_address(REGISTRY_ADDRESS), abi=registry_abi)
token = w3.eth.contract(address=Web3.to_checksum_address(TOKEN_ADDRESS), abi=token_abi)

# ---------------- Owner Setup ----------------
DEFAULT_HARDHAT_KEY = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
OWNER_KEY = os.getenv("PRIVATE_KEY", DEFAULT_HARDHAT_KEY)
if not OWNER_KEY.startswith("0x"):
    OWNER_KEY = "0x" + OWNER_KEY

try:
    accounts = w3.eth.accounts
    OWNER = accounts[0] if len(accounts) > 0 else None
except Exception:
    OWNER = None

if not OWNER:
    acct = w3.eth.account.from_key(OWNER_KEY)
    OWNER = acct.address

OWNER = Web3.to_checksum_address(OWNER)

# ---------------- Models ----------------
class Project(BaseModel):
    name: str
    location: str
    hectares: int
    owner: str
    metadata: str

class UploadRequest(BaseModel):
    project_id: int
    uploader: str
    gps: str
    co2: float
    evidence_type: str = "general"  # "before", "after", "general"
    project_area_hectares: Optional[float] = None
    time_period_years: float = 1.0

class VerifyRequest(BaseModel):
    evidence_id: int
    mint_receipt: bool = False   # ✅ boolean (fix)
    receipt_token_uri: str = ""
    mint_amount: int = 0

class MintRequest(BaseModel):
    project_id: int
    amount: int

# ---------------- Auth Models ----------------
class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str
    role: str = "user"
    organization_name: Optional[str] = None
    wallet_address: Optional[str] = None

class AuthResponse(BaseModel):
    access_token: str
    token_type: str
    user: dict

# ---------------- Auth Security ----------------
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """Get current authenticated user from JWT token"""
    token = credentials.credentials
    payload = AuthService.verify_token(token)
    
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    user = AuthService.get_user_by_id(payload["user_id"])
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user

def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """Require admin role"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

# ---------------- Helpers ----------------
def to_checksum(address: str) -> str:
    try:
        return Web3.to_checksum_address(address)
    except Exception:
        raise HTTPException(status_code=400, detail=f"Invalid Ethereum address: {address}")

def clean(o: Any):
    if isinstance(o, HexBytes): return o.hex()
    if isinstance(o, bytes): return "0x" + o.hex()
    if isinstance(o, (list, tuple)): return [clean(x) for x in o]
    if isinstance(o, dict): return {k: clean(v) for k, v in o.items()}
    if hasattr(o, "_asdict"): return {k: clean(v) for k, v in o._asdict().items()}
    if hasattr(o, "__dict__"): return {k: clean(v) for k, v in vars(o).items()}
    return o

def sign_and_send(tx: dict):
    try:
        signed = w3.eth.account.sign_transaction(tx, private_key=OWNER_KEY)
        raw = signed.raw_transaction
        tx_hash = w3.eth.send_raw_transaction(raw)
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        return Web3.to_hex(tx_hash), clean(dict(receipt))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transaction failed: {e}")

# ---------------- Routes ----------------
@app.get("/status")
def get_status():
    try:
        total_supply = token.functions.totalSupply().call()
    except Exception:
        total_supply = None
    return clean({
        "connected": w3.is_connected(),
        "registry": REGISTRY_ADDRESS,
        "token": TOKEN_ADDRESS,
        "owner": OWNER,
        "totalSupply": total_supply,
    })

# ---------------- Auth Routes ----------------
@app.post("/auth/login", response_model=AuthResponse)
def login(request: LoginRequest):
    """Authenticate user and return JWT token"""
    user = AuthService.authenticate_user(request.username, request.password)
    
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    access_token = AuthService.create_access_token(
        user_id=user.id,
        username=user.username,
        role=user.role.value
    )
    
    return AuthResponse(
        access_token=access_token,
        token_type="bearer",
        user={
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role.value,
            "organization_name": user.organization_name,
            "wallet_address": user.wallet_address
        }
    )

@app.post("/auth/register", response_model=AuthResponse)
def register(request: RegisterRequest):
    """Register a new user"""
    try:
        # Map string role to enum
        role_map = {
            "user": UserRole.USER,
            "admin": UserRole.ADMIN,
            "ngo": UserRole.NGO
        }
        role = role_map.get(request.role.lower(), UserRole.USER)
        
        user = AuthService.create_user(
            username=request.username,
            email=request.email,
            password=request.password,
            role=role,
            organization_name=request.organization_name,
            wallet_address=request.wallet_address
        )
        
        access_token = AuthService.create_access_token(
            user_id=user.id,
            username=user.username,
            role=user.role.value
        )
        
        return AuthResponse(
            access_token=access_token,
            token_type="bearer",
            user={
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role.value,
                "organization_name": user.organization_name,
                "wallet_address": user.wallet_address
            }
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/auth/me")
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role.value,
        "organization_name": current_user.organization_name,
        "wallet_address": current_user.wallet_address
    }

class WalletUpdateRequest(BaseModel):
    wallet_address: str

@app.put("/auth/wallet")
def update_wallet_address(
    wallet_request: WalletUpdateRequest,
    current_user: User = Depends(get_current_user)
):
    """Update user's wallet address"""
    db = SessionLocal()
    try:
        # Validate wallet address format (basic check)
        wallet_address = wallet_request.wallet_address.strip()
        if not wallet_address.startswith('0x') or len(wallet_address) != 42:
            raise HTTPException(status_code=400, detail="Invalid wallet address format")
        
        # Check if wallet address is already in use
        existing_user = db.query(User).filter(
            User.wallet_address == wallet_address,
            User.id != current_user.id
        ).first()
        
        if existing_user:
            raise HTTPException(status_code=400, detail="Wallet address already in use")
        
        # Update wallet address
        current_user.wallet_address = wallet_address
        db.commit()
        
        return {"message": "Wallet address updated successfully", "wallet_address": wallet_address}
    finally:
        db.close()

@app.get("/admin/users")
def get_all_users(current_user: User = Depends(require_admin)):
    """Get all users (admin only)"""
    db = SessionLocal()
    try:
        users = db.query(User).all()
        return [
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role.value,
                "organization_name": user.organization_name,
                "wallet_address": user.wallet_address,
                "is_active": user.is_active,
                "created_at": user.created_at.isoformat()
            }
            for user in users
        ]
    finally:
        db.close()

# ---------------- Existing Routes ----------------

@app.get("/projects/my")
def get_my_projects(current_user: User = Depends(get_current_user)):
    """Get projects owned by the current user with full details"""
    try:
        total = registry.functions.totalProjects().call()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read totalProjects: {e}")

    projects = []
    # Use the specific wallet address for filtering
    target_wallet = "0xa114791A6a939087048960f48e62fbe817828CD1"
    
    for i in range(1, total + 1):
        try:
            p = registry.functions.projects(i).call()
        except Exception:
            continue

        # Only include projects owned by the specific wallet address
        if p[3].lower() == target_wallet.lower():
            # fetch evidences from DB for this project
            db = SessionLocal()
            rows = db.query(MRVData).filter(MRVData.project_id == i).all()
            db.close()
            evidences = [
                {
                    "evidenceId": r.id,
                    "projectId": r.project_id,
                    "uploader": r.uploader,
                    "gps": r.gps,
                    "co2": r.co2,
                    "mediaHashes": r.media_hashes,
                    "evidenceHash": r.evidence_hash,
                    "timestamp": r.timestamp.isoformat()
                } for r in rows
            ]

            projects.append({
                "id": i,
                "name": p[0],
                "location": p[1],
                "hectares": p[2],
                "owner": p[3],
                "metadata": p[4],
                "exists": p[5],
                "totalIssuedCredits": p[6],
                "evidences": evidences
            })

    return clean(projects)

@app.get("/projects/all")
def get_all_projects_limited(current_user: User = Depends(get_current_user)):
    """Get all projects with limited info for NGO users (only address and latest credit timeframe)"""
    try:
        total = registry.functions.totalProjects().call()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read totalProjects: {e}")

    projects = []
    # Use the specific wallet address for filtering
    target_wallet = "0xa114791A6a939087048960f48e62fbe817828CD1"
    
    for i in range(1, total + 1):
        try:
            p = registry.functions.projects(i).call()
        except Exception:
            continue

        # For admin users, show full details
        if current_user.role == UserRole.ADMIN:
            # fetch evidences from DB for this project
            db = SessionLocal()
            rows = db.query(MRVData).filter(MRVData.project_id == i).all()
            db.close()
            evidences = [
                {
                    "evidenceId": r.id,
                    "projectId": r.project_id,
                    "uploader": r.uploader,
                    "gps": r.gps,
                    "co2": r.co2,
                    "mediaHashes": r.media_hashes,
                    "evidenceHash": r.evidence_hash,
                    "timestamp": r.timestamp.isoformat()
                } for r in rows
            ]

            projects.append({
                "id": i,
                "name": p[0],
                "location": p[1],
                "hectares": p[2],
                "owner": p[3],
                "metadata": p[4],
                "exists": p[5],
                "totalIssuedCredits": p[6],
                "evidences": evidences
            })
        else:
            # For NGO users, only show limited info for projects they don't own
            if p[3].lower() != target_wallet.lower():
                # Get latest evidence timestamp for timeframe info
                db = SessionLocal()
                latest_evidence = db.query(MRVData).filter(MRVData.project_id == i).order_by(MRVData.timestamp.desc()).first()
                db.close()
                
                latest_timeframe = latest_evidence.timestamp.isoformat() if latest_evidence else None
                
                projects.append({
                    "id": i,
                    "owner": p[3],  # Only crypto address
                    "totalIssuedCredits": p[6],
                    "latestCreditTimeframe": latest_timeframe,
                    "isLimited": True  # Flag to indicate limited data
                })

    return clean(projects)

@app.get("/projects")
def get_projects():
    """Legacy endpoint - returns all projects with full details (for backwards compatibility)"""
    try:
        total = registry.functions.totalProjects().call()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read totalProjects: {e}")

    projects = []
    for i in range(1, total + 1):
        try:
            p = registry.functions.projects(i).call()
        except Exception:
            continue

        # fetch evidences from DB for this project
        db = SessionLocal()
        rows = db.query(MRVData).filter(MRVData.project_id == i).all()
        db.close()
        evidences = [
            {
                "evidenceId": r.id,
                "projectId": r.project_id,
                "uploader": r.uploader,
                "gps": r.gps,
                "co2": r.co2,
                "mediaHashes": r.media_hashes,
                "evidenceHash": r.evidence_hash,
                "timestamp": r.timestamp.isoformat()
            } for r in rows
        ]

        projects.append({
            "id": i,
            "name": p[0],
            "location": p[1],
            "hectares": p[2],
            "owner": p[3],
            "metadata": p[4],
            "exists": p[5],
            "totalIssuedCredits": p[6],
            "evidences": evidences
        })

    return clean(projects)

@app.post("/projects")
def register_project(project: Project):
    owner_checksum = to_checksum(project.owner)
    try:
        tx = registry.functions.registerProject(
            project.name,
            project.location,
            project.hectares,
            owner_checksum,
            project.metadata
        ).build_transaction({
            "from": OWNER,
            "nonce": w3.eth.get_transaction_count(OWNER),
            "gas": 2_000_000,
            "gasPrice": w3.to_wei("20", "gwei")
        })
        tx_hash, receipt = sign_and_send(tx)
        return clean({"status": "ok", "tx_hash": tx_hash, "receipt": receipt})
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to build transaction: {e}")

@app.delete("/projects/{project_id}")
def delete_project(project_id: int, current_user: User = Depends(get_current_user)):
    """Delete a project and all its associated evidence"""
    try:
        # First, verify the project exists and get project details
        project_data = registry.functions.projects(project_id).call()
        if not project_data[5]:  # exists field
            raise HTTPException(status_code=404, detail="Project not found")
        
        # Check if user is admin or project owner
        project_owner = project_data[3]
        if current_user.role != UserRole.ADMIN and current_user.wallet_address.lower() != project_owner.lower():
            raise HTTPException(status_code=403, detail="You don't have permission to delete this project")
        
        # Delete all evidence from database
        db = SessionLocal()
        try:
            # Delete all MRV data associated with this project
            deleted_evidence = db.query(MRVData).filter(MRVData.project_id == project_id).delete()
            db.commit()
            
            # Note: We can't actually delete the project from the blockchain contract
            # as it would break the indexing. Instead, we mark it as deleted by setting exists=false
            # This would require a contract modification to add a deleteProject function
            
            return clean({
                "status": "success", 
                "message": f"Project {project_id} evidence deleted successfully",
                "deleted_evidence_count": deleted_evidence,
                "note": "Project still exists on blockchain but evidence has been removed"
            })
            
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {e}")
        finally:
            db.close()
            
    except Exception as e:
        if "Project not found" in str(e) or "permission" in str(e):
            raise e
        raise HTTPException(status_code=500, detail=f"Failed to delete project: {e}")

@app.post("/upload")
async def upload_evidence(
    project_id: int = Form(...),
    uploader: str = Form(...),
    gps: str = Form(...),
    co2: float = Form(...),
    evidence_type: str = Form("general"),  # "before", "after", "general", "before_after_pair"
    project_area_hectares: Optional[float] = Form(None),
    time_period_years: float = Form(1.0),
    files: List[UploadFile] = File(None)
):
    """
    Upload evidence files with support for before/after image analysis.
    For AI-based carbon credit calculation, both before and after images are required.
    """
    # Validate evidence type
    valid_evidence_types = ["before", "after", "general", "before_after_pair"]
    if evidence_type not in valid_evidence_types:
        raise HTTPException(status_code=400, detail=f"Invalid evidence_type. Must be one of: {valid_evidence_types}")
    
    # For before/after analysis, project area is required
    if evidence_type in ["before", "after", "before_after_pair"] and project_area_hectares is None:
        raise HTTPException(status_code=400, detail="project_area_hectares is required for before/after evidence")
    
    # Save files locally
    os.makedirs("uploads", exist_ok=True)
    saved_files = []
    file_data = {}
    
    for f in files or []:
        path = os.path.join("uploads", f.filename)
        file_content = await f.read()
        
        # Save file
        with open(path, "wb") as buffer:
            buffer.write(file_content)
        saved_files.append(path)
        
        # Store file data for AI analysis
        file_data[f.filename] = file_content

    # Compute sha256 hash
    m = hashlib.sha256()
    for path in saved_files:
        with open(path, "rb") as fh: 
            m.update(fh.read())
    evidence_hash_bytes = m.digest()

    metadata = json.dumps({
        "gps": gps, 
        "co2": co2, 
        "evidence_type": evidence_type,
        "project_area_hectares": project_area_hectares,
        "time_period_years": time_period_years,
        "files": [os.path.basename(p) for p in saved_files]
    })

    # Blockchain transaction
    tx = registry.functions.uploadEvidence(project_id, evidence_hash_bytes, metadata).build_transaction({
        "from": OWNER,
        "nonce": w3.eth.get_transaction_count(OWNER),
        "gas": 2_000_000,
        "gasPrice": w3.to_wei("20", "gwei")
    })
    tx_hash, receipt = sign_and_send(tx)

    # Get evidence_id
    evidence_id = None
    try:
        events = registry.events.EvidenceUploaded().processReceipt(receipt)
        if events: 
            evidence_id = int(events[0]["args"]["evidenceId"])
    except Exception:
        pass

    # Store in database with enhanced fields
    db = SessionLocal()
    try:
        # Create MRV record with new fields
        record = MRVData(
            project_id=project_id,
            uploader=uploader,
            gps=gps,
            co2=str(co2),  # Legacy field
            media_hashes={"files": [os.path.basename(p) for p in saved_files]},
            evidence_hash="0x" + evidence_hash_bytes.hex(),
            verified=False,
            
            # New fields
            evidence_type=evidence_type,
            project_area_hectares=project_area_hectares,
            
            # Placeholder for AI analysis results (will be updated during verification)
            calculated_co2_sequestration=None,
            vegetation_change_percentage=None,
            ndvi_improvement=None,
            land_transformation_score=None,
            calculated_carbon_credits=None,
            credit_calculation_method='pending_analysis',
            ai_analysis_results=None,
            confidence_score=None,
            analysis_summary=None
        )
        
        db.add(record)
        db.commit()
        db.refresh(record)
        
        db_id = record.id
        
    except Exception as e:
        db.rollback()
        logger.error(f"Database error during upload: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        db.close()

    # Check for paired before/after evidence for AI analysis
    ai_analysis_result = None
    if evidence_type == "before_after_pair":
        # Both images uploaded together - immediate AI analysis
        if len(file_data) >= 2:
            file_names = list(file_data.keys())
            ai_analysis_result = await perform_immediate_ai_analysis(
                project_id, file_data[file_names[0]], file_data[file_names[1]], 
                project_area_hectares, time_period_years
            )
    elif evidence_type in ["before", "after"]:
        # Traditional paired analysis (look for complementary evidence)
        ai_analysis_result = await attempt_paired_analysis(
            project_id, evidence_type, file_data, project_area_hectares, time_period_years
        )

    # Prepare response
    response = {
        "status": "ok",
        "tx_hash": tx_hash,
        "evidence_hash": "0x" + evidence_hash_bytes.hex(),
        "evidence_id": evidence_id or db_id,
        "metadata": metadata,
        "files": saved_files,
        "db_id": db_id,
        "evidence_type": evidence_type,
        "project_area_hectares": project_area_hectares
    }
    
    # Include AI analysis result if available
    if ai_analysis_result:
        response["ai_analysis"] = ai_analysis_result
        response["dynamic_credits_calculated"] = ai_analysis_result.get('success', False)
        if ai_analysis_result.get('success'):
            response["recommended_credits"] = ai_analysis_result.get('recommended_credits', 0)
            response["provisional_credits"] = ai_analysis_result.get('provisional_credits', 0)
            response["deferred_credits"] = ai_analysis_result.get('deferred_credits', 0)
            response["credit_distribution"] = ai_analysis_result.get('credit_distribution', {})
            response["monitoring_requirements"] = ai_analysis_result.get('monitoring_requirements', [])
            response["calculation_method"] = ai_analysis_result.get('calculation_method', 'ai_analysis')

    return clean(response)

@app.post("/estimate-carbon-credits")
async def estimate_carbon_credits(
    project_area_hectares: float = Form(...),
    time_period_years: float = Form(1.0),
    ecosystem_type: str = Form("mangrove"),  # "mangrove", "seagrass", "saltmarsh", "mixed"
    before_image: Optional[UploadFile] = File(None),
    after_image: Optional[UploadFile] = File(None)
):
    """
    Provide real-time estimation of carbon credits before formal submission.
    Analyzes uploaded images and project parameters to give immediate feedback.
    """
    try:
        # Validate inputs
        if project_area_hectares <= 0:
            raise HTTPException(status_code=400, detail="Project area must be greater than 0")
        
        if time_period_years <= 0:
            raise HTTPException(status_code=400, detail="Time period must be greater than 0")
        
        valid_ecosystems = ["mangrove", "seagrass", "saltmarsh", "mixed"]
        if ecosystem_type not in valid_ecosystems:
            raise HTTPException(status_code=400, detail=f"Invalid ecosystem type. Must be one of: {valid_ecosystems}")
        
        # Initialize response with basic calculation
        response = {
            "status": "success",
            "estimation_type": "basic",
            "project_area_hectares": project_area_hectares,
            "time_period_years": time_period_years,
            "ecosystem_type": ecosystem_type,
            "estimated_credits": 0,
            "co2_sequestration_kg": 0,
            "calculation_method": "baseline",
            "confidence_level": "medium",
            "breakdown": {}
        }
        
        # Basic calculation using CO2 sequestration rates
        from services.co2_sequestration_calculator import CO2SequestrationCalculator
        co2_calculator = CO2SequestrationCalculator()
        
        # Calculate baseline CO2 sequestration
        baseline_co2 = co2_calculator.calculate_basic_co2_sequestration(
            ecosystem_type=ecosystem_type,
            area_hectares=project_area_hectares,
            time_period_years=time_period_years,
            transformation_factor=1.0  # Assume moderate transformation
        )
        
        # Basic credit calculation: CO2 Sequestered (kg) * Area (hectares) * conversion factor
        baseline_credits = baseline_co2 * project_area_hectares * 0.001  # Convert to appropriate scale
        
        response.update({
            "estimated_credits": round(baseline_credits, 2),
            "co2_sequestration_kg": round(baseline_co2, 2),
            "breakdown": {
                "base_sequestration_rate": co2_calculator.base_rates.get(ecosystem_type, 1000),
                "area_factor": project_area_hectares,
                "time_factor": time_period_years,
                "transformation_assumption": "moderate (50-70% improvement)"
            }
        })
        
        # If both images are provided, perform AI analysis
        if before_image and after_image:
            try:
                # Read image data
                before_image_data = await before_image.read()
                after_image_data = await after_image.read()
                
                # Validate image formats
                if not before_image.content_type.startswith('image/'):
                    raise HTTPException(status_code=400, detail="Before image must be an image file")
                if not after_image.content_type.startswith('image/'):
                    raise HTTPException(status_code=400, detail="After image must be an image file")
                
                # Perform AI analysis for more accurate estimation
                from services.dynamic_carbon_credit_calculator import DynamicCarbonCreditCalculator
                ai_calculator = DynamicCarbonCreditCalculator()
                
                ai_result = ai_calculator.calculate_dynamic_credits(
                    before_image_data=before_image_data,
                    after_image_data=after_image_data,
                    project_area_hectares=project_area_hectares,
                    time_period_years=time_period_years,
                    project_metadata={
                        "ecosystem_type": ecosystem_type,
                        "estimation_mode": True
                    }
                )
                
                if ai_result.get('success'):
                    # Update response with AI analysis results including provisional credits
                    response.update({
                        "estimation_type": "ai_enhanced",
                        "estimated_credits": ai_result.get('recommended_credits', baseline_credits),
                        "provisional_credits": ai_result.get('provisional_credits', 0),
                        "deferred_credits": ai_result.get('deferred_credits', 0),
                        "co2_sequestration_kg": ai_result.get('supporting_analysis', {}).get('co2_sequestration', {}).get('co2_sequestration_kg', baseline_co2),
                        "calculation_method": ai_result.get('calculation_method', 'ai_analysis'),
                        "confidence_level": "high" if ai_result.get('verification_confidence', 0) > 0.8 else "medium",
                        "credit_distribution": ai_result.get('credit_distribution', {}),
                        "monitoring_requirements": ai_result.get('monitoring_requirements', []),
                        "ai_analysis": {
                            "vegetation_change": ai_result.get('supporting_analysis', {}).get('transformation_metrics', {}).get('vegetation_change_percentage', 0),
                            "ndvi_improvement": ai_result.get('supporting_analysis', {}).get('transformation_metrics', {}).get('ndvi_improvement', 0),
                            "transformation_score": ai_result.get('supporting_analysis', {}).get('transformation_metrics', {}).get('transformation_score', 0),
                            "confidence_score": ai_result.get('verification_confidence', 0),
                            "summary": ai_result.get('calculation_summary', 'AI analysis completed')
                        }
                    })
                    
                    # Enhanced breakdown with AI insights and provisional credit info
                    response["breakdown"].update({
                        "provisional_system": f"Immediate: {ai_result.get('provisional_credits', 0):.1f} credits, Deferred: {ai_result.get('deferred_credits', 0):.1f} credits",
                        "ai_vegetation_analysis": f"{ai_result.get('supporting_analysis', {}).get('transformation_metrics', {}).get('vegetation_change_percentage', 0):.1f}% vegetation improvement",
                        "ndvi_score": f"{ai_result.get('supporting_analysis', {}).get('transformation_metrics', {}).get('ndvi_improvement', 0):.3f} NDVI improvement",
                        "transformation_quality": ai_result.get('supporting_analysis', {}).get('transformation_metrics', {}).get('quality_assessment', 'moderate')
                    })
                else:
                    # AI analysis failed, add warning but keep baseline calculation
                    response["warnings"] = [f"AI analysis failed: {ai_result.get('error', 'Unknown error')}"]
                    response["confidence_level"] = "low"
            
            except Exception as ai_error:
                # AI analysis error, fall back to baseline but notify user
                response["warnings"] = [f"AI analysis unavailable: {str(ai_error)}"]
                response["confidence_level"] = "low"
        
        else:
            # Only basic calculation available
            response["notes"] = [
                "Upload both before and after images for AI-enhanced estimation",
                "Current estimate is based on ecosystem averages and may vary significantly"
            ]
        
        # Add estimation disclaimer
        response["disclaimer"] = "This is an estimate only. Final credits will be calculated during formal verification process."
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Estimation failed: {str(e)}")

async def perform_immediate_ai_analysis(project_id: int, before_image_data: bytes, 
                                      after_image_data: bytes, project_area_hectares: float,
                                      time_period_years: float) -> Optional[Dict]:
    """
    Perform immediate AI analysis when both before and after images are uploaded together.
    """
    try:
        from services.dynamic_carbon_credit_calculator import DynamicCarbonCreditCalculator
        
        # Perform AI analysis
        calculator = DynamicCarbonCreditCalculator()
        analysis_result = calculator.calculate_dynamic_credits(
            before_image_data=before_image_data,
            after_image_data=after_image_data,
            project_area_hectares=project_area_hectares,
            time_period_years=time_period_years,
            project_metadata={"project_id": project_id, "analysis_type": "immediate_pair"}
        )
        
        if analysis_result.get('success'):
            # Update database record with analysis results
            db = SessionLocal()
            try:
                # Find the most recent record for this project
                current_evidence = db.query(MRVData).filter(
                    MRVData.project_id == project_id
                ).order_by(MRVData.id.desc()).first()
                
                if current_evidence:
                    supporting_analysis = analysis_result.get('supporting_analysis', {})
                    transformation_metrics = supporting_analysis.get('transformation_metrics', {})
                    co2_results = supporting_analysis.get('co2_sequestration', {})
                    
                    # Update with analysis results including provisional credits
                    current_evidence.calculated_co2_sequestration = co2_results.get('co2_sequestration_kg')
                    current_evidence.vegetation_change_percentage = transformation_metrics.get('vegetation_change_percentage')
                    current_evidence.ndvi_improvement = transformation_metrics.get('ndvi_improvement')
                    current_evidence.land_transformation_score = transformation_metrics.get('transformation_score')
                    current_evidence.calculated_carbon_credits = analysis_result.get('recommended_credits')
                    current_evidence.credit_calculation_method = analysis_result.get('calculation_method', 'ai_analysis_immediate')
                    current_evidence.ai_analysis_results = analysis_result
                    current_evidence.confidence_score = analysis_result.get('verification_confidence')
                    current_evidence.analysis_summary = analysis_result.get('calculation_summary')
                    
                    db.commit()
                    
                provisional_credits = analysis_result.get('provisional_credits', 0)
                deferred_credits = analysis_result.get('deferred_credits', 0)
                logger.info(f"Immediate AI analysis completed for project {project_id}. Total: {analysis_result.get('recommended_credits')} credits (Provisional: {provisional_credits}, Deferred: {deferred_credits})")
                return analysis_result
                
            except Exception as db_error:
                db.rollback()
                logger.error(f"Database error in immediate analysis: {db_error}")
                # Return analysis result even if DB update fails
                return analysis_result
            finally:
                db.close()
        else:
            logger.error(f"Immediate AI analysis failed: {analysis_result.get('error')}")
            return analysis_result
            
    except Exception as e:
        logger.error(f"Error in immediate AI analysis: {e}")
        return {"success": False, "error": str(e)}

async def attempt_paired_analysis(project_id: int, current_evidence_type: str, 
                                current_file_data: Dict, project_area_hectares: float,
                                time_period_years: float) -> Optional[Dict]:
    """
    Attempt to find paired before/after evidence and perform AI analysis.
    """
    try:
        db = SessionLocal()
        
        # Look for the complementary evidence type
        complementary_type = "after" if current_evidence_type == "before" else "before"
        
        # Find existing evidence of complementary type for this project
        complementary_evidence = db.query(MRVData).filter(
            MRVData.project_id == project_id,
            MRVData.evidence_type == complementary_type,
            MRVData.project_area_hectares == project_area_hectares
        ).order_by(MRVData.timestamp.desc()).first()
        
        if not complementary_evidence:
            logger.info(f"No {complementary_type} evidence found for project {project_id}. Waiting for pair.")
            return None
        
        # Load the complementary image data
        complementary_files = complementary_evidence.media_hashes.get('files', [])
        if not complementary_files:
            logger.warning(f"No files found in {complementary_type} evidence")
            return None
        
        # Load the first image file from complementary evidence
        complementary_file_path = os.path.join("uploads", complementary_files[0])
        if not os.path.exists(complementary_file_path):
            logger.warning(f"Complementary file not found: {complementary_file_path}")
            return None
        
        with open(complementary_file_path, "rb") as f:
            complementary_file_data = f.read()
        
        # Get current image data (assume first file is the main image)
        current_file_names = list(current_file_data.keys())
        if not current_file_names:
            logger.warning("No current file data available")
            return None
        
        current_image_data = current_file_data[current_file_names[0]]
        
        # Determine before and after image data
        if current_evidence_type == "before":
            before_image_data = current_image_data
            after_image_data = complementary_file_data
        else:
            before_image_data = complementary_file_data
            after_image_data = current_image_data
        
        # Perform AI analysis
        calculator = DynamicCarbonCreditCalculator()
        analysis_result = calculator.calculate_dynamic_credits(
            before_image_data=before_image_data,
            after_image_data=after_image_data,
            project_area_hectares=project_area_hectares,
            time_period_years=time_period_years,
            project_metadata={"project_id": project_id}
        )
        
        if analysis_result.get('success'):
            # Update both evidence records with analysis results
            supporting_analysis = analysis_result.get('supporting_analysis', {})
            transformation_metrics = supporting_analysis.get('transformation_metrics', {})
            co2_results = supporting_analysis.get('co2_sequestration', {})
            
            # Update current evidence
            current_evidence = db.query(MRVData).filter(MRVData.project_id == project_id).order_by(MRVData.id.desc()).first()
            if current_evidence:
                current_evidence.calculated_co2_sequestration = co2_results.get('co2_sequestration_kg')
                current_evidence.vegetation_change_percentage = transformation_metrics.get('vegetation_change_percentage')
                current_evidence.ndvi_improvement = transformation_metrics.get('ndvi_improvement')
                current_evidence.land_transformation_score = transformation_metrics.get('transformation_score')
                current_evidence.calculated_carbon_credits = analysis_result.get('recommended_credits')
                current_evidence.credit_calculation_method = 'ai_analysis'
                current_evidence.ai_analysis_results = analysis_result
                current_evidence.confidence_score = analysis_result.get('verification_confidence')
                current_evidence.analysis_summary = analysis_result.get('calculation_summary')
            
            # Update complementary evidence
            complementary_evidence.calculated_co2_sequestration = co2_results.get('co2_sequestration_kg')
            complementary_evidence.vegetation_change_percentage = transformation_metrics.get('vegetation_change_percentage')
            complementary_evidence.ndvi_improvement = transformation_metrics.get('ndvi_improvement')
            complementary_evidence.land_transformation_score = transformation_metrics.get('transformation_score')
            complementary_evidence.calculated_carbon_credits = analysis_result.get('recommended_credits')
            complementary_evidence.credit_calculation_method = 'ai_analysis'
            complementary_evidence.ai_analysis_results = analysis_result
            complementary_evidence.confidence_score = analysis_result.get('verification_confidence')
            complementary_evidence.analysis_summary = analysis_result.get('calculation_summary')
            
            # Store image hashes for reference
            if current_evidence_type == "before":
                current_evidence.before_image_hash = current_evidence.evidence_hash
                current_evidence.after_image_hash = complementary_evidence.evidence_hash
                complementary_evidence.before_image_hash = current_evidence.evidence_hash
                complementary_evidence.after_image_hash = complementary_evidence.evidence_hash
            else:
                current_evidence.after_image_hash = current_evidence.evidence_hash
                current_evidence.before_image_hash = complementary_evidence.evidence_hash
                complementary_evidence.after_image_hash = current_evidence.evidence_hash
                complementary_evidence.before_image_hash = complementary_evidence.evidence_hash
            
            db.commit()
            
            logger.info(f"AI analysis completed for project {project_id}. Recommended credits: {analysis_result.get('recommended_credits')}")
            return analysis_result
        else:
            logger.error(f"AI analysis failed: {analysis_result.get('error')}")
            return analysis_result
            
    except Exception as e:
        db.rollback()
        logger.error(f"Error in paired analysis: {e}")
        return {"success": False, "error": str(e)}
    finally:
        db.close()

@app.get("/evidences/{project_id}")
def get_evidences_for_project(project_id: int):
    db = SessionLocal()
    rows = db.query(MRVData).filter(MRVData.project_id == project_id).all()
    db.close()
    return clean([
        {
            "evidenceId": r.id,
            "projectId": r.project_id,
            "uploader": r.uploader,
            "gps": r.gps,
            "co2": r.co2,
            "mediaHashes": r.media_hashes,
            "evidenceHash": r.evidence_hash,
            "timestamp": r.timestamp.isoformat(),
            "verified": r.verified or False
        } for r in rows
    ])

@app.post("/verify")
def verify_project(req: VerifyRequest):
    """
    Verify project evidence and issue carbon credits.
    Uses AI-calculated credits when available, falls back to specified amount.
    """
    evidence_id = int(req.evidence_id)
    
    # Get evidence details from database
    db = SessionLocal()
    try:
        evidence = db.query(MRVData).filter(MRVData.id == evidence_id).first()
        if not evidence:
            raise HTTPException(status_code=404, detail="Evidence not found")
        
        # Determine credit amount to mint
        credits_to_mint = 0
        calculation_method = "fixed"
        analysis_report = None
        
        # Check if AI-calculated credits are available
        if (evidence.calculated_carbon_credits is not None and 
            evidence.credit_calculation_method == 'ai_analysis' and
            evidence.confidence_score is not None):
            
            # Use AI-calculated credits
            credits_to_mint = int(evidence.calculated_carbon_credits)
            calculation_method = "ai_analysis"
            analysis_report = evidence.analysis_summary
            
            logger.info(f"Using AI-calculated credits: {credits_to_mint} for evidence {evidence_id}")
            
        elif req.mint_amount and req.mint_amount > 0:
            # Use manually specified amount
            credits_to_mint = int(req.mint_amount)
            calculation_method = "manual_override"
            
            logger.info(f"Using manual credit amount: {credits_to_mint} for evidence {evidence_id}")
            
        else:
            # Fall back to legacy fixed amount
            credits_to_mint = 100
            calculation_method = "legacy_fixed"
            
            logger.info(f"Using legacy fixed credits: {credits_to_mint} for evidence {evidence_id}")
        
        # Validation: ensure reasonable credit amounts
        if credits_to_mint < 0:
            credits_to_mint = 0
        elif credits_to_mint > 10000:  # Safety cap
            logger.warning(f"Credit amount {credits_to_mint} exceeds safety cap, capping at 10000")
            credits_to_mint = 10000
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        db.close()
    
    # Build blockchain verification transaction
    try:
        tx = registry.functions.verifyEvidenceAndIssue(
            evidence_id,
            req.mint_receipt,
            req.receipt_token_uri or "",
            credits_to_mint
        ).build_transaction({
            "from": OWNER,
            "nonce": w3.eth.get_transaction_count(OWNER),
            "gas": 2_000_000,
            "gasPrice": w3.to_wei("20", "gwei")
        })
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to build verify transaction: {e}")

    # Execute transaction
    tx_hash, receipt = sign_and_send(tx)

    # Update evidence verification status in database
    db = SessionLocal()
    try:
        evidence = db.query(MRVData).filter(MRVData.id == evidence_id).first()
        if evidence:
            evidence.verified = True
            db.commit()
            
            # Get updated project info
            project_id = evidence.project_id
            project = registry.functions.projects(project_id).call()
            
            # Prepare comprehensive verification result
            verification_result = {
                "status": "verified",
                "tx_hash": tx_hash,
                "receipt": receipt,
                "evidence_id": evidence_id,
                "credits_issued": credits_to_mint,
                "calculation_method": calculation_method,
                "project": {
                    "id": project_id,
                    "name": project[0],
                    "location": project[1],
                    "hectares": project[2],
                    "owner": project[3],
                    "metadata": project[4],
                    "exists": project[5],
                    "totalIssuedCredits": project[6]
                }
            }
            
            # Include AI analysis details if available
            if calculation_method == "ai_analysis" and evidence.ai_analysis_results:
                verification_result["ai_analysis"] = {
                    "co2_sequestration_kg": evidence.calculated_co2_sequestration,
                    "vegetation_change_percentage": evidence.vegetation_change_percentage,
                    "ndvi_improvement": evidence.ndvi_improvement,
                    "land_transformation_score": evidence.land_transformation_score,
                    "confidence_score": evidence.confidence_score,
                    "evidence_type": evidence.evidence_type,
                    "project_area_hectares": evidence.project_area_hectares,
                    "calculation_summary": analysis_report,
                    "detailed_analysis": evidence.ai_analysis_results
                }
                
                # Include verification level and recommendations
                ai_results = evidence.ai_analysis_results
                if isinstance(ai_results, dict):
                    verification_result["verification_level"] = ai_results.get('verification_level', 'unknown')
                    verification_result["recommended_action"] = ai_results.get('recommended_action', 'unknown')
                    verification_result["verification_confidence"] = ai_results.get('verification_confidence', 0)
            
            logger.info(f"Project {project_id} verified successfully. Credits issued: {credits_to_mint}")
            return clean(verification_result)
            
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to update evidence verification status: {e}")
        # Still return success since blockchain transaction succeeded
        return clean({
            "status": "verified_with_db_warning",
            "tx_hash": tx_hash,
            "receipt": receipt,
            "credits_issued": credits_to_mint,
            "calculation_method": calculation_method,
            "db_warning": str(e)
        })
    finally:
        db.close()

@app.post("/mint")
def mint_credits(req: MintRequest):
    try:
        tx = token.functions.mint(
            OWNER,
            req.amount
        ).build_transaction({
            "from": OWNER,
            "nonce": w3.eth.get_transaction_count(OWNER),
            "gas": 200000,
            "gasPrice": w3.to_wei("20", "gwei")
        })
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to build mint transaction: {e}")

    tx_hash, receipt = sign_and_send(tx)

    # ✅ fetch updated balance
    balance = token.functions.balanceOf(OWNER).call()

    return clean({
        "status": "minted",
        "tx_hash": tx_hash,
        "receipt": receipt,
        "balance": balance
    })
@app.get("/projects/{project_id}")
def get_project(project_id: int):
    try:
        p = registry.functions.projects(project_id).call()
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Project not found: {e}")

    evidences = []
    try:
        ev_event = registry.events.EvidenceUploaded()
        logs = w3.eth.get_logs({
            "fromBlock": 0,
            "toBlock": "latest",
            "address": REGISTRY_ADDRESS
        })
        for log in logs:
            processed = ev_event.processLog(log)
            if processed["args"]["projectId"] == project_id:
                evidences.append({
                    "evidenceId": int(processed["args"]["evidenceId"]),
                    "evidenceHash": processed["args"]["evidenceHash"].hex(),
                    "evidenceURI": processed["args"]["evidenceURI"],
                    "uploader": processed["args"]["uploader"],
                    "txHash": processed["transactionHash"].hex(),
                    "blockNumber": processed["blockNumber"]
                })
    except Exception:
        evidences = []

    return {
        "id": project_id,
        "name": p[0],
        "location": p[1],
        "hectares": p[2],
        "owner": p[3],
        "metadata": p[4],
        "exists": p[5],
        "totalIssuedCredits": p[6],
        "evidences": evidences
    }

@app.get("/credits/{address}")
def get_credits(address: str):
    addr = to_checksum(address)
    try:
        balance = token.functions.balanceOf(addr).call()
        return clean({"address": addr, "balance": balance})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch balance: {e}")

# New AI-Enhanced Endpoints

@app.get("/evidences/{evidence_id}/analysis")
def get_evidence_analysis(evidence_id: int):
    """
    Get detailed AI analysis results for a specific evidence.
    """
    db = SessionLocal()
    try:
        evidence = db.query(MRVData).filter(MRVData.id == evidence_id).first()
        if not evidence:
            raise HTTPException(status_code=404, detail="Evidence not found")
        
        result = {
            "evidence_id": evidence_id,
            "project_id": evidence.project_id,
            "evidence_type": evidence.evidence_type,
            "project_area_hectares": evidence.project_area_hectares,
            "calculated_co2_sequestration": evidence.calculated_co2_sequestration,
            "vegetation_change_percentage": evidence.vegetation_change_percentage,
            "ndvi_improvement": evidence.ndvi_improvement,
            "land_transformation_score": evidence.land_transformation_score,
            "calculated_carbon_credits": evidence.calculated_carbon_credits,
            "credit_calculation_method": evidence.credit_calculation_method,
            "confidence_score": evidence.confidence_score,
            "analysis_summary": evidence.analysis_summary,
            "verified": evidence.verified,
            "timestamp": evidence.timestamp.isoformat() if evidence.timestamp else None
        }
        
        # Include detailed AI results if available
        if evidence.ai_analysis_results:
            result["detailed_analysis"] = evidence.ai_analysis_results
            
        return clean(result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get analysis: {e}")
    finally:
        db.close()

@app.get("/projects/{project_id}/credit-calculation")
def get_project_credit_calculation(project_id: int):
    """
    Get comprehensive credit calculation details for a project.
    """
    db = SessionLocal()
    try:
        # Get all evidence for the project
        evidences = db.query(MRVData).filter(MRVData.project_id == project_id).all()
        
        if not evidences:
            raise HTTPException(status_code=404, detail="No evidence found for project")
        
        # Organize evidence by type
        evidence_by_type = {}
        total_credits = 0
        ai_analyzed_credits = 0
        
        for evidence in evidences:
            evidence_type = evidence.evidence_type or 'general'
            if evidence_type not in evidence_by_type:
                evidence_by_type[evidence_type] = []
            
            evidence_info = {
                "evidence_id": evidence.id,
                "timestamp": evidence.timestamp.isoformat() if evidence.timestamp else None,
                "calculated_credits": evidence.calculated_carbon_credits,
                "calculation_method": evidence.credit_calculation_method,
                "confidence_score": evidence.confidence_score,
                "verified": evidence.verified
            }
            
            evidence_by_type[evidence_type].append(evidence_info)
            
            if evidence.calculated_carbon_credits:
                if evidence.credit_calculation_method == 'ai_analysis':
                    ai_analyzed_credits += evidence.calculated_carbon_credits
                total_credits += evidence.calculated_carbon_credits
        
        # Get project details from blockchain
        try:
            project = registry.functions.projects(project_id).call()
            project_info = {
                "id": project_id,
                "name": project[0],
                "location": project[1],
                "hectares": project[2],
                "owner": project[3],
                "metadata": project[4],
                "exists": project[5],
                "totalIssuedCredits": project[6]
            }
        except Exception:
            project_info = {"id": project_id, "error": "Could not fetch project details"}
        
        # Analyze credit calculation patterns
        has_before_after = 'before' in evidence_by_type and 'after' in evidence_by_type
        calculation_summary = {
            "total_evidence_count": len(evidences),
            "evidence_types": list(evidence_by_type.keys()),
            "has_before_after_analysis": has_before_after,
            "total_calculated_credits": total_credits,
            "ai_analyzed_credits": ai_analyzed_credits,
            "percentage_ai_analyzed": (ai_analyzed_credits / total_credits * 100) if total_credits > 0 else 0
        }
        
        return clean({
            "project_info": project_info,
            "evidence_by_type": evidence_by_type,
            "calculation_summary": calculation_summary
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get credit calculation: {e}")
    finally:
        db.close()

@app.post("/projects/{project_id}/trigger-analysis")
async def trigger_manual_analysis(project_id: int, project_area_hectares: float):
    """
    Manually trigger AI analysis for a project if before/after evidence exists.
    """
    db = SessionLocal()
    try:
        # Find before and after evidence
        before_evidence = db.query(MRVData).filter(
            MRVData.project_id == project_id,
            MRVData.evidence_type == 'before'
        ).order_by(MRVData.timestamp.desc()).first()
        
        after_evidence = db.query(MRVData).filter(
            MRVData.project_id == project_id,
            MRVData.evidence_type == 'after'
        ).order_by(MRVData.timestamp.desc()).first()
        
        if not before_evidence or not after_evidence:
            raise HTTPException(
                status_code=400, 
                detail="Both before and after evidence required for analysis"
            )
        
        # Load image files
        before_files = before_evidence.media_hashes.get('files', [])
        after_files = after_evidence.media_hashes.get('files', [])
        
        if not before_files or not after_files:
            raise HTTPException(status_code=400, detail="Image files not found for analysis")
        
        # Load image data
        before_file_path = os.path.join("uploads", before_files[0])
        after_file_path = os.path.join("uploads", after_files[0])
        
        if not os.path.exists(before_file_path) or not os.path.exists(after_file_path):
            raise HTTPException(status_code=400, detail="Image files not accessible")
        
        with open(before_file_path, "rb") as f:
            before_image_data = f.read()
        
        with open(after_file_path, "rb") as f:
            after_image_data = f.read()
        
        # Perform AI analysis
        calculator = DynamicCarbonCreditCalculator()
        analysis_result = calculator.calculate_dynamic_credits(
            before_image_data=before_image_data,
            after_image_data=after_image_data,
            project_area_hectares=project_area_hectares,
            time_period_years=1.0,
            project_metadata={"project_id": project_id, "manual_trigger": True}
        )
        
        if analysis_result.get('success'):
            # Update both evidence records
            supporting_analysis = analysis_result.get('supporting_analysis', {})
            transformation_metrics = supporting_analysis.get('transformation_metrics', {})
            co2_results = supporting_analysis.get('co2_sequestration', {})
            
            for evidence in [before_evidence, after_evidence]:
                evidence.project_area_hectares = project_area_hectares
                evidence.calculated_co2_sequestration = co2_results.get('co2_sequestration_kg')
                evidence.vegetation_change_percentage = transformation_metrics.get('vegetation_change_percentage')
                evidence.ndvi_improvement = transformation_metrics.get('ndvi_improvement')
                evidence.land_transformation_score = transformation_metrics.get('transformation_score')
                evidence.calculated_carbon_credits = analysis_result.get('recommended_credits')
                evidence.credit_calculation_method = 'ai_analysis_manual'
                evidence.ai_analysis_results = analysis_result
                evidence.confidence_score = analysis_result.get('verification_confidence')
                evidence.analysis_summary = analysis_result.get('calculation_summary')
                evidence.before_image_hash = before_evidence.evidence_hash
                evidence.after_image_hash = after_evidence.evidence_hash
            
            db.commit()
            
            return clean({
                "success": True,
                "message": "AI analysis completed successfully",
                "analysis_result": analysis_result,
                "updated_evidence_ids": [before_evidence.id, after_evidence.id]
            })
        else:
            return clean({
                "success": False,
                "error": analysis_result.get('error', 'Analysis failed'),
                "analysis_result": analysis_result
            })
            
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Analysis failed: {e}")
    finally:
        db.close()

@app.get("/system/ai-verification-stats")
def get_ai_verification_stats():
    """
    Get system-wide AI verification statistics.
    """
    db = SessionLocal()
    try:
        # Count evidence by calculation method
        total_evidence = db.query(MRVData).count()
        ai_analyzed = db.query(MRVData).filter(MRVData.credit_calculation_method == 'ai_analysis').count()
        manual_override = db.query(MRVData).filter(MRVData.credit_calculation_method == 'manual_override').count()
        legacy_fixed = db.query(MRVData).filter(MRVData.credit_calculation_method == 'legacy_fixed').count()
        pending_analysis = db.query(MRVData).filter(MRVData.credit_calculation_method == 'pending_analysis').count()
        
        # Count evidence by type
        before_evidence = db.query(MRVData).filter(MRVData.evidence_type == 'before').count()
        after_evidence = db.query(MRVData).filter(MRVData.evidence_type == 'after').count()
        general_evidence = db.query(MRVData).filter(MRVData.evidence_type == 'general').count()
        
        # Calculate average confidence score for AI-analyzed evidence
        ai_evidence = db.query(MRVData).filter(
            MRVData.credit_calculation_method == 'ai_analysis',
            MRVData.confidence_score.isnot(None)
        ).all()
        
        avg_confidence = 0
        total_ai_credits = 0
        if ai_evidence:
            confidences = [e.confidence_score for e in ai_evidence if e.confidence_score]
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            
            credits = [e.calculated_carbon_credits for e in ai_evidence if e.calculated_carbon_credits]
            total_ai_credits = sum(credits) if credits else 0
        
        return clean({
            "evidence_statistics": {
                "total_evidence": total_evidence,
                "ai_analyzed": ai_analyzed,
                "manual_override": manual_override,
                "legacy_fixed": legacy_fixed,
                "pending_analysis": pending_analysis
            },
            "evidence_types": {
                "before_evidence": before_evidence,
                "after_evidence": after_evidence,
                "general_evidence": general_evidence
            },
            "ai_analysis_metrics": {
                "average_confidence_score": round(avg_confidence, 2),
                "total_ai_calculated_credits": round(total_ai_credits, 2),
                "ai_adoption_percentage": round((ai_analyzed / total_evidence * 100) if total_evidence > 0 else 0, 2)
            },
            "system_health": {
                "has_paired_analysis": before_evidence > 0 and after_evidence > 0,
                "analysis_coverage": round((ai_analyzed / total_evidence * 100) if total_evidence > 0 else 0, 2)
            }
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get statistics: {e}")
    finally:
        db.close()

# Include AI Verification Router
app.include_router(ai_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
