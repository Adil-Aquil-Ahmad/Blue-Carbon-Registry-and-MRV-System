import os

# Blockchain config
RPC_URL = "http://127.0.0.1:8545"
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

# Default to Hardhat private key if not set
if not PRIVATE_KEY:
    PRIVATE_KEY = "0xdf57089febbacf7ba0bc227dafbffa9fc08a93fdc68e1e42411a14efcf23656e"  

CONTRACT_ADDRESS = "0x5FbDB2315678afecb367f032d93F642f64180aa3"  # Update after deploy
CONTRACT_ABI_PATH = "contracts/BlueCarbonRegistry.json"

# Database config
DB_URL = f"sqlite:///{os.path.abspath('bluecarbon.db')}"

# IPFS config
IPFS_HOST = "/ip4/127.0.0.1/tcp/5001/http"
