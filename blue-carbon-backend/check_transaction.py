from web3 import Web3

w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))

tx_hash = '0x413021d5c8cca71155051d738dc71273c1a31a838c2b25f9ad2bdc5fd9e99194'

try:
    receipt = w3.eth.get_transaction_receipt(tx_hash)
    print(f'Transaction status: {receipt.status}')
    print(f'Gas used: {receipt.gasUsed}')
    print(f'Logs: {len(receipt.logs)}')
    
    if receipt.status == 1:
        print("✅ Transaction succeeded")
    else:
        print("❌ Transaction failed")
        
    # Get the actual transaction
    tx = w3.eth.get_transaction(tx_hash)
    print(f"Transaction to: {tx['to']}")
    print(f"Transaction data: {tx['input'][:100]}...")
    
except Exception as e:
    print(f'Error getting receipt: {e}')