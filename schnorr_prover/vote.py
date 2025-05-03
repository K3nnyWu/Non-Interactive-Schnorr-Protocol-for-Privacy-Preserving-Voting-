from web3 import Web3
from eth_account.messages import encode_defunct
import json

# Connect to local Hardhat node
w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))

# Select a funded account from Hardhat defaults
w3.eth.default_account = w3.eth.accounts[0]  # First pre-funded account

# Verify account balance
account = w3.eth.default_account
balance = w3.eth.get_balance(account)
print(f"Using account: {account}, Balance: {balance} wei")

# Use the private key of the first Hardhat account
private_key = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"

# Create a message to sign
message = "Vote from " + account
message_hash = Web3.keccak(text=message)

# Sign the message with the funded account's private key using encode_defunct
signable_message = encode_defunct(text=message)
signature = w3.eth.account.sign_message(signable_message, private_key=private_key).signature

# Load contract ABI and address
contract_address = "0x5FbDB2315678afecb367f032d93F642f64180aa3"
with open('../artifacts/contracts/PrivateVoting.sol/PrivateVoting.json') as f:
    contract_artifact = json.load(f)
    abi = contract_artifact['abi']
contract = w3.eth.contract(address=contract_address, abi=abi)

# Get the latest nonce, including pending transactions
nonce = w3.eth.get_transaction_count(account, 'pending')
print(f"Using nonce: {nonce}")

# Build the transaction with the correct nonce
tx = contract.functions.vote(
    signature,
    message_hash
).build_transaction({
    'gas': 50000,
    'nonce': nonce,
    'gasPrice': w3.eth.gas_price
})

# Sign and send the transaction
try:
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Vote successful! TX Hash: {tx_hash.hex()}")
except Exception as e:
    print(f"Error sending transaction: {e}")