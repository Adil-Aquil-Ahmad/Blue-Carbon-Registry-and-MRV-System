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

print("Checking recent blockchain evidence...")

# Check evidence for project 1
for evidence_id in range(1, 10):
    try:
        evidence = contract.functions.evidence(evidence_id).call()
        if evidence[2]:  # exists field
            print(f"Evidence {evidence_id}: Project={evidence[0]}, Hash={evidence[1][:20]}..., Exists={evidence[2]}")
    except Exception as e:
        break

print("\nChecking project 1 evidence count...")
try:
    project1 = contract.functions.projects(1).call()
    print(f"Project 1 total credits: {project1[6]}")
except Exception as e:
    print(f"Error: {e}")