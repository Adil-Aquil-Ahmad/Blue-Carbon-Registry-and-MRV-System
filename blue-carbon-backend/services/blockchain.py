from web3 import Web3
import json
from config import RPC_URL, PRIVATE_KEY, CONTRACT_ADDRESS, CONTRACT_ABI_PATH

w3 = Web3(Web3.HTTPProvider(RPC_URL))
account = w3.eth.account.from_key(PRIVATE_KEY)

with open(CONTRACT_ABI_PATH) as f:
    contract_json = json.load(f)
abi = contract_json["abi"]
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)

def register_project(name: str, description: str):
    tx = contract.functions.registerProject(name, description).buildTransaction({
        'from': account.address,
        'gas': 3000000,
        'nonce': w3.eth.get_transaction_count(account.address)
    })
    signed_tx = account.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return receipt

def issue_credit(project_id: int, carbon_amount: int):
    tx = contract.functions.issueCredits(project_id, carbon_amount).buildTransaction({
        'from': account.address,
        'gas': 3000000,
        'nonce': w3.eth.get_transaction_count(account.address)
    })
    signed_tx = account.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return receipt
