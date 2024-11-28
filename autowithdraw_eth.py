import database as db
from web3 import Web3
import time
from config import send_address, gwei_eth, eth_min_balance

# Web3 configuration for Ethereum
eth_node_url = "https://eth-rpc.gateway.pokt.network"
web3 = Web3(Web3.HTTPProvider(eth_node_url))
processed_blocks = set()

def process_eth_blocks():
    """Fetch and process new blocks from Ethereum."""
    while True:
        latest_block = web3.eth.get_block(block_identifier=web3.eth.defaultBlock, full_transactions=True)
        if latest_block.number not in processed_blocks:
            processed_blocks.add(latest_block.number)
            transactions = latest_block.transactions
            print(f'Processing Block #{latest_block.number} | ETH')
            process_transactions_eth(transactions)
        time.sleep(0.3)

def process_transactions_eth(transactions):
    """Identify and handle transactions for monitored addresses."""
    for tx in transactions:
        try:
            destination_address = tx['to']
            if db.is_address_monitored(destination_address):
                handle_transaction_eth(destination_address)
        except Exception as e:
            print(f"Error processing transaction: {e}")
            continue

def handle_transaction_eth(address):
    """Handle withdrawal from a monitored Ethereum address."""
    try:
        balance = web3.eth.get_balance(address)
        gas_price = web3.toWei(gwei_eth, 'gwei')
        min_balance_wei = web3.toWei(eth_min_balance, 'ether')

        if balance < min_balance_wei:
            print(f"Insufficient balance for address: {address}")
            return

        private_key = db.get_private_key(address)
        nonce = web3.eth.get_transaction_count(address)
        gas_limit = 21000
        gas_cost = gas_price * gas_limit
        transfer_amount = balance - gas_cost

        tx_details = {
            'chainId': 1,
            'nonce': nonce,
            'to': send_address,
            'value': transfer_amount,
            'gas': gas_limit,
            'gasPrice': gas_price
        }

        signed_tx = web3.eth.account.sign_transaction(tx_details, private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f"ETH Withdrawal Successful | TX Hash: {web3.toHex(tx_hash)} | Address: {address}")
    except Exception as e:
        print(f"Error in withdrawal process for address {address}: {e}")

if __name__ == '__main__':
    process_eth_blocks()
