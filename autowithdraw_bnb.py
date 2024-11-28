import database as db
from web3 import Web3
from web3.middleware import geth_poa_middleware
import time
from config import send_address, gwei_bnb, bnb_min_balance

# Web3 configuration for Binance Smart Chain
bnb_node_url = "https://bsc-dataseed1.binance.org/"
web3 = Web3(Web3.HTTPProvider(bnb_node_url))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

def process_bnb_blocks():
    """Fetch and process new blocks from Binance Smart Chain."""
    last_processed_block = 0
    while True:
        latest_block = web3.eth.get_block(block_identifier=web3.eth.defaultBlock, full_transactions=True)
        if last_processed_block == latest_block.number:
            continue
        last_processed_block = latest_block.number
        transactions = latest_block.transactions
        print(f'Processing Block #{latest_block.number} | BNB')
        process_transactions_bnb(transactions)
        time.sleep(0.1)

def process_transactions_bnb(transactions):
    """Identify and handle transactions for monitored addresses."""
    for tx in transactions:
        try:
            destination_address = tx['to']
            if db.is_address_monitored(destination_address):
                handle_transaction_bnb(destination_address)
        except Exception as e:
            print(f"Error processing transaction: {e}")
            continue

def handle_transaction_bnb(address):
    """Handle withdrawal from a monitored Binance Smart Chain address."""
    try:
        balance = web3.eth.get_balance(address)
        gas_price = web3.toWei(gwei_bnb, 'gwei')
        min_balance_wei = web3.toWei(bnb_min_balance, 'ether')

        if balance < min_balance_wei:
            print(f"Insufficient balance for address: {address}")
            return

        private_key = db.get_private_key(address)
        nonce = web3.eth.get_transaction_count(address)
        gas_limit = 21000
        gas_cost = gas_price * gas_limit
        transfer_amount = balance - gas_cost

        tx_details = {
            'chainId': 56,
            'nonce': nonce,
            'to': send_address,
            'value': transfer_amount,
            'gas': gas_limit,
            'gasPrice': gas_price
        }

        signed_tx = web3.eth.account.sign_transaction(tx_details, private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f"BNB Withdrawal Successful | TX Hash: {web3.toHex(tx_hash)} | Address: {address}")
    except Exception as e:
        print(f"Error in withdrawal process for address {address}: {e}")

if __name__ == '__main__':
    process_bnb_blocks()
