import os
from web3 import Web3
import json
import ipfshttpclient
from database import SessionLocal
from models.db_model import MRVData

from config import RPC_URL, PRIVATE_KEY, CONTRACT_ADDRESS, CONTRACT_ABI_PATH

# -----------------------------
# Blockchain Setup & Test
# -----------------------------
print("=== Blockchain Test ===")
w3 = Web3(Web3.HTTPProvider(RPC_URL))
print("Connected to blockchain:", w3.is_connected())

# Load account
account = w3.eth.account.from_key(PRIVATE_KEY)
print("Account address:", account.address)
balance = w3.eth.get_balance(account.address)
print("Account balance (ether):", w3.from_wei(balance, "ether"))

# Load contract
with open(CONTRACT_ABI_PATH, "r") as f:
    contract_json = json.load(f)
abi = contract_json["abi"]
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)

# Call a read function (example: totalProjects or similar)
try:
    total_projects = contract.functions.totalProjects().call()
    print("Total projects in registry:", total_projects)
except Exception as e:
    print("Contract read failed:", e)

# -----------------------------
# IPFS Upload Test
# -----------------------------
print("\n=== IPFS Test ===")
try:
    client = ipfshttpclient.connect("/ip4/127.0.0.1/tcp/5001/http")
    res = client.add_str("Test data for blue carbon MRV")
    print("IPFS upload successful! CID:", res)
except Exception as e:
    print("IPFS upload failed:", e)

# -----------------------------
# Database Test
# -----------------------------
print("\n=== Database Test ===")
db = SessionLocal()
try:
    record = MRVData(
        project_id=1,
        uploader="Test User",
        gps_coordinates="12.9716,77.5946",
        co2_sequestered=123.45,
        media_hashes=[res]  # from IPFS test
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    print("Database insert successful! ID:", record.id)
except Exception as e:
    print("Database insert failed:", e)
finally:
    db.close()

print("\n=== ALL TESTS COMPLETED ===")
