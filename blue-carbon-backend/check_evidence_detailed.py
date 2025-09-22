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

print("Checking evidence with correct method...")

# The contract might have a different evidence structure
# Let me check what functions are available
for item in contract_data['abi']:
    if item.get('type') == 'function' and 'evidence' in item.get('name', '').lower():
        print(f"Evidence function: {item['name']}")

# Try different ways to check evidence
print("\nTrying to get evidence count or list...")

# Check if there's an evidence counter
try:
    # Some contracts have evidenceCounter
    counter = contract.functions.evidenceCounter().call()
    print(f"Evidence counter: {counter}")
except:
    pass

# Check recent blocks for events
print("\nChecking recent transaction events...")
tx_hash = '0x413021d5c8cca71155051d738dc71273c1a31a838c2b25f9ad2bdc5fd9e99194'
receipt = w3.eth.get_transaction_receipt(tx_hash)

# Parse logs
for log in receipt.logs:
    try:
        parsed = contract.events.EvidenceUploaded().processLog(log)
        print(f"EvidenceUploaded event: {parsed['args']}")
    except:
        pass
        
print(f"\nTotal logs in transaction: {len(receipt.logs)}")
if receipt.logs:
    print(f"First log topics: {receipt.logs[0]['topics']}")