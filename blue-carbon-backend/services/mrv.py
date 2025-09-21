from database import SessionLocal
from models.db_model import MRVData
import requests

IPFS_API = "http://127.0.0.1:5001/api/v0/"
IPFS_GATEWAY = "http://127.0.0.1:8080/ipfs/"

def add_file_to_ipfs(file_obj):
    """Upload a file-like object to IPFS and return the CID."""
    files = {"file": (file_obj.filename, file_obj.file)}
    response = requests.post(IPFS_API + "add", files=files)
    response.raise_for_status()
    return response.json()["Hash"]

def upload_field_data(project_id: int, uploader: str, gps: str, co2: float, files: list):
    """Upload MRV field data along with media to IPFS and store record in DB."""
    media_hashes = []
    for file in files:
        cid = add_file_to_ipfs(file)
        media_hashes.append(cid)

    db = SessionLocal()
    record = MRVData(
        project_id=project_id,
        uploader=uploader,
        gps=gps,               # ✅ corrected field
        co2=co2,               # ✅ corrected field
        media_hashes=media_hashes,
        evidence_hash=""       # optional, set later if needed
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    db.close()
    return record

def get_file_from_ipfs(cid, output_path):
    """Download a file from IPFS using its CID."""
    url = f"{IPFS_GATEWAY}{cid}"
    response = requests.get(url)
    response.raise_for_status()
    with open(output_path, "wb") as f:
        f.write(response.content)
