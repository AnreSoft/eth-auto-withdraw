![GH-preview](https://github.com/user-attachments/assets/3b0c02fc-66f6-4de5-abab-39698102d476)
# Etherium Wallet Automation Tool

## Overview
This tool is designed to monitor and manage crypto wallet addresses on Ethereum and Binance Smart Chain (BSC). It automates the following processes:
- Parsing and storing wallet seed phrases.
- Monitoring blockchain transactions for specified addresses.
- Automatically withdrawing balances from monitored wallets.

## Features
- **Blockchain Integration**: Supports Ethereum and Binance Smart Chain using Web3.
- **Seed Phrase Management**: Parses and securely stores wallet addresses and private keys.
- **Automated Withdrawals**: Automatically transfers funds from monitored addresses to a specified destination address.
- **Threaded Execution**: Efficiently processes transactions in parallel using threading.
- **Customizable Settings**: Configure gas prices, minimum balances, and withdrawal destination.

---

## Installation

### Prerequisites
- Python 3.8 or later
- Pip (Python package installer)

### Required Libraries
Install dependencies using the following command:
```bash
pip install web3 hdwallet
```

# Configuration

Edit the `config.py` file to set your preferences:

- **send_address**: The destination address for withdrawals.
- **gwei_eth / gwei_bnb**: Gas price for Ethereum and Binance Smart Chain transactions (in Gwei).
- **eth_min_balance / bnb_min_balance**: Minimum balance required for withdrawal (in Ether/BNB).

### Example:
```python
send_address = "0xYourWalletAddressHere"
gwei_eth = 40
gwei_bnb = 40
eth_min_balance = 0.0005
bnb_min_balance = 0.0005
```

# Usage

## 1. Initialize the Database
If no database exists, it will be automatically created when the tool runs. The database (`seeds.db`) stores wallet addresses and encrypted private keys.

---

## 2. Parse Seed Files
Place `.txt` files containing seed phrases in the `wallets` directory. Each line in the file should contain one seed phrase.

---

## 3. Start the Tool
Run the `main.py` file:
```bash
python main.py
```

