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

print("Checking evidence using correct functions...")

# From the transaction log, evidenceId looks like it's 8 (0x08)
evidence_ids = [1, 2, 3, 4, 5, 6, 7, 8]

for evidence_id in evidence_ids:
    try:
        # Try evidences function
        evidence = contract.functions.evidences(evidence_id).call()
        print(f"Evidence {evidence_id}: {evidence}")
    except Exception as e:
        if "execution reverted" not in str(e):
            print(f"Error checking evidence {evidence_id}: {e}")

print("\nTrying getEvidence function...")
for evidence_id in evidence_ids:
    try:
        evidence = contract.functions.getEvidence(evidence_id).call()
        print(f"Evidence {evidence_id}: {evidence}")
    except Exception as e:
        if "execution reverted" not in str(e):
            print(f"Error checking evidence {evidence_id}: {e}")

# Check the event logs more carefully
print("\nDecoding transaction event...")
tx_hash = '0x413021d5c8cca71155051d738dc71273c1a31a838c2b25f9ad2bdc5fd9e99194'
receipt = w3.eth.get_transaction_receipt(tx_hash)

# The topics show evidenceId=8, projectId=1
topics = receipt.logs[0]['topics']
evidence_id = int(topics[1].hex(), 16)
project_id = int(topics[2].hex(), 16)

print(f"Event: EvidenceUploaded(evidenceId={evidence_id}, projectId={project_id})")

# Now check that specific evidence
try:
    evidence = contract.functions.evidences(evidence_id).call()
    print(f"Evidence {evidence_id} details: {evidence}")
except Exception as e:
    print(f"Could not read evidence {evidence_id}: {e}")