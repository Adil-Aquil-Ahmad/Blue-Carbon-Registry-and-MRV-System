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

# Check projects 1-10 to see which ones exist
print("Checking blockchain projects:")
for i in range(1, 11):
    try:
        project = contract.functions.projects(i).call()
        if project[5]:  # exists field
            print(f'Project {i}: Name="{project[0]}", Location="{project[1]}", Area={project[2]}, Owner={project[3]}, Exists={project[5]}, TotalCredits={project[6]}')
        else:
            print(f'Project {i}: Does not exist')
    except Exception as e:
        print(f'Error reading project {i}: {e}')
        break