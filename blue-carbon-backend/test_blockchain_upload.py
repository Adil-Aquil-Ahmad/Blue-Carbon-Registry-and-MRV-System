from web3 import Web3
import json

# Connect to blockchain
w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))

# Load contract
with open('contracts/BlueCarbonRegistry.json', 'r') as f:
    contract_data = json.load(f)

contract = w3.eth.contract(
    address='0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512',
    abi=contract_data['abi']
)

print("Testing blockchain connection...")
print(f"Connected: {w3.is_connected()}")
print(f"Chain ID: {w3.eth.chain_id}")

print("\nTesting contract calls...")

# Test reading project 1
try:
    project1 = contract.functions.projects(1).call()
    print(f"Project 1: {project1}")
    print(f"Project 1 exists: {project1[5]}")
except Exception as e:
    print(f"Error reading project 1: {e}")

# Test reading project 2  
try:
    project2 = contract.functions.projects(2).call()
    print(f"Project 2: {project2}")
    print(f"Project 2 exists: {project2[5]}")
except Exception as e:
    print(f"Error reading project 2: {e}")

# Test if evidence upload would work with project 1
test_hash = b'\x12\x34\x56\x78' * 8  # 32 bytes
test_metadata = "test"

try:
    # Just estimate gas, don't actually send
    gas_estimate = contract.functions.uploadEvidence(1, test_hash, test_metadata).estimate_gas({'from': '0x8626f6940E2eb28930eFb4CeF49B2d1F2C9C1199'})
    print(f"Gas estimate for project 1: {gas_estimate}")
except Exception as e:
    print(f"Error estimating gas for project 1: {e}")

try:
    # Test with project 2
    gas_estimate = contract.functions.uploadEvidence(2, test_hash, test_metadata).estimate_gas({'from': '0x8626f6940E2eb28930eFb4CeF49B2d1F2C9C1199'})
    print(f"Gas estimate for project 2: {gas_estimate}")
except Exception as e:
    print(f"Error estimating gas for project 2: {e}")