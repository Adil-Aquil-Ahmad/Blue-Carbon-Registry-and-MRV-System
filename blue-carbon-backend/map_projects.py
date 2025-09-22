#!/usr/bin/env python3
"""
Simple script to map existing database projects to blockchain projects
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal
from models.db_model import ProjectData

# Import blockchain connection from main.py
from web3 import Web3
import json

# Blockchain config
RPC_URL = "http://127.0.0.1:8545"
w3 = Web3(Web3.HTTPProvider(RPC_URL))

# Contract setup
REGISTRY_ADDRESS = "0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512"
with open("contracts/BlueCarbonRegistry.json", "r") as f:
    contract_data = json.load(f)
registry = w3.eth.contract(address=REGISTRY_ADDRESS, abi=contract_data["abi"])

def map_projects():
    """Map database projects to existing blockchain projects"""
    print("🔗 Mapping Database Projects to Blockchain Projects")
    print("=" * 60)
    
    db = SessionLocal()
    try:
        # Get projects without blockchain_id
        db_projects = db.query(ProjectData).filter(
            ProjectData.blockchain_id.is_(None)
        ).all()
        
        print(f"📊 Found {len(db_projects)} database projects to map")
        
        # Get blockchain projects
        try:
            total_blockchain = registry.functions.totalProjects().call()
            print(f"📊 Found {total_blockchain} blockchain projects")
        except Exception as e:
            print(f"❌ Failed to read blockchain: {e}")
            return
        
        # Map each database project
        for db_project in db_projects:
            print(f"\n🔍 Mapping: {db_project.name} (Owner: {db_project.owner})")
            
            # Search for matching blockchain project
            found_match = False
            for i in range(1, total_blockchain + 1):
                try:
                    blockchain_data = registry.functions.projects(i).call()
                    bc_name = blockchain_data[0]
                    bc_owner = blockchain_data[3]
                    
                    # Simple name matching (case insensitive)
                    if bc_name.lower() == db_project.name.lower():
                        print(f"✅ Found match: Blockchain ID {i}")
                        print(f"   Name: {bc_name}")
                        print(f"   Blockchain Owner: {bc_owner}")
                        print(f"   Database Owner: {db_project.owner}")
                        
                        # Update database
                        db_project.blockchain_id = i
                        db_project.verified_on_blockchain = True
                        db.commit()
                        found_match = True
                        break
                        
                except Exception as e:
                    print(f"⚠️  Error reading blockchain project {i}: {e}")
            
            if not found_match:
                print(f"❌ No blockchain match found for: {db_project.name}")
        
        print(f"\n✅ Mapping completed!")
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    map_projects()