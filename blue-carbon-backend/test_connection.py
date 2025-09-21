from web3 import Web3
from config import RPC_URL, PRIVATE_KEY

w3 = Web3(Web3.HTTPProvider(RPC_URL))
print("Connected:", w3.is_connected())  # <-- call the method

account = w3.eth.account.from_key(PRIVATE_KEY)
print("Account address:", account.address)

# Optional: check balance
balance = w3.eth.get_balance(account.address)
print("Account balance (wei):", balance)
print("Account balance (ether):", w3.from_wei(balance, 'ether'))