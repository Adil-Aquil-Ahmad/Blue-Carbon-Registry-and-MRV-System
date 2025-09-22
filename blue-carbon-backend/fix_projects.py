#!/usr/bin/env python3
"""
Fix existing projects by registering them on the blockchain
This script handles projects that were saved to database but failed blockchain registration
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal
from models.db_model import ProjectData
from config import PRIVATE_KEY as HARDHAT_PRIVATE_KEY, RPC_URL as HARDHAT_RPC_URL
from web3 import Web3
from hexbytes import HexBytes
import json

# Initialize Web3
w3 = Web3(Web3.HTTPProvider(HARDHAT_RPC_URL))
OWNER = w3.eth.account.from_key(HARDHAT_PRIVATE_KEY).address

# Load contract
with open("contracts/BlueCarbonRegistry.json", "r") as f:
    contract_data = json.load(f)

# Use the latest deployment address
REGISTRY_ADDRESS = "0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512"  # Updated to match main.py
registry = w3.eth.contract(address=REGISTRY_ADDRESS, abi=contract_data["abi"])

def to_checksum(address):
    """Convert address to checksum format"""
    return w3.to_checksum_address(address)

def sign_and_send(tx):
    """Sign and send transaction"""
    signed = w3.eth.account.sign_transaction(tx, HARDHAT_PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return tx_hash.hex(), receipt

def fix_project_registration():
    """Fix projects that don't have blockchain_id"""
    db = SessionLocal()
    try:
        # Find projects without blockchain_id
        projects_to_fix = db.query(ProjectData).filter(
            ProjectData.blockchain_id.is_(None)
        ).all()
        
        print(f"Found {len(projects_to_fix)} projects to fix:")
        
        for project in projects_to_fix:
            print(f"\nFixing project: {project.name} (ID: {project.id})")
            print(f"Owner: {project.owner}")
            
            try:
                # Register project on blockchain
                owner_checksum = to_checksum(project.owner)
                
                tx = registry.functions.registerProject(
                    project.name,
                    project.location,
                    project.hectares,
                    owner_checksum,
                    project.project_metadata or ""
                ).build_transaction({
                    "from": OWNER,
                    "nonce": w3.eth.get_transaction_count(OWNER),
                    "gas": 2_000_000,
                    "gasPrice": w3.to_wei("20", "gwei")
                })
                
                tx_hash, receipt = sign_and_send(tx)
                
                # Try to get blockchain project ID from events
                blockchain_project_id = None
                try:
                    project_events = registry.events.ProjectRegistered().process_receipt(receipt)
                    if project_events:
                        blockchain_project_id = int(project_events[0]["args"]["projectId"])
                        print(f"✅ Registered on blockchain with ID: {blockchain_project_id}")
                    else:
                        # Fallback: use total projects count
                        total_projects = registry.functions.totalProjects().call()
                        blockchain_project_id = total_projects
                        print(f"✅ Using total projects count as ID: {blockchain_project_id}")
                except Exception as e:
                    print(f"⚠️  Could not extract project ID from events: {e}")
                    # Fallback: use total projects count
                    try:
                        total_projects = registry.functions.totalProjects().call()
                        blockchain_project_id = total_projects
                        print(f"✅ Using total projects count as fallback ID: {blockchain_project_id}")
                    except Exception as fallback_error:
                        print(f"❌ Failed to get blockchain project ID: {fallback_error}")
                        continue
                
                # Update database record
                project.blockchain_id = blockchain_project_id
                project.tx_hash = tx_hash
                project.verified_on_blockchain = True
                
                db.commit()
                print(f"✅ Updated database record with blockchain ID: {blockchain_project_id}")
                
            except Exception as e:
                print(f"❌ Failed to register project {project.name}: {e}")
                db.rollback()
                continue
        
        print(f"\n🎉 Finished processing {len(projects_to_fix)} projects")
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        db.rollback()
    finally:
        db.close()

def check_blockchain_projects():
    """Check what projects exist on the blockchain"""
    try:
        total = registry.functions.totalProjects().call()
        print(f"\nTotal projects on blockchain: {total}")
        
        for i in range(1, total + 1):
            try:
                p = registry.functions.projects(i).call()
                print(f"Project {i}: {p[0]} at {p[1]} ({p[2]} hectares) - Owner: {p[3]}")
            except Exception as e:
                print(f"Error reading project {i}: {e}")
                
    except Exception as e:
        print(f"Error checking blockchain projects: {e}")

if __name__ == "__main__":
    print("🔧 Blue Carbon Project Fix Utility")
    print("=" * 50)
    
    # Check current state
    print("\n📊 Current blockchain state:")
    check_blockchain_projects()
    
    # Fix projects
    print("\n🔧 Fixing project registrations:")
    fix_project_registration()
    
    # Check final state
    print("\n📊 Final blockchain state:")
    check_blockchain_projects()
    
    print("\n✅ Project fix completed!")