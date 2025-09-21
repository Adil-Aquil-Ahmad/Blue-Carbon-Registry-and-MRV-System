import os

# Blockchain config
RPC_URL = "http://127.0.0.1:8545"
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

# Default to Hardhat first account private key if not set
if not PRIVATE_KEY:
    PRIVATE_KEY = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"  

CONTRACT_ADDRESS = "0x5FbDB2315678afecb367f032d93F642f64180aa3"  # Update after deploy
CONTRACT_ABI_PATH = "contracts/BlueCarbonRegistry.json"

# Database config
DB_URL = "sqlite:///./bluecarbon.db"

# IPFS config
IPFS_HOST = "/ip4/127.0.0.1/tcp/5001/http"
