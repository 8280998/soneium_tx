import json
import time
import random
from web3 import Web3
from eth_account import Account

# 配置
INFURA_URL = "https://rpc.soneium.org"  # Soneium RPC URL
PRIVATE_KEY_FILE = "address.txt"  # 私钥文件（每行一个私钥）
VELODROME_CONTRACT_ADDRESS = "0x4200000000000000000000000000000000000006"
ABI_FILE = "abi.json"
CHAIN_ID = 1868
MAX_BASE_FEE = int(0.00100026 * 10**9)
PRIORITY_FEE = int(0.00100026 * 10**9)
GAS_LIMIT = 36194

# 连接到RPC网络
web3 = Web3(Web3.HTTPProvider(INFURA_URL))
if not web3.is_connected():
    raise Exception("连接失败。。。")

# 加载ABI
with open(ABI_FILE, 'r') as file:
    velodrome_abi = json.load(file)

# 创建Velodrome合约对象
velodrome_contract = web3.eth.contract(address=VELODROME_CONTRACT_ADDRESS, abi=velodrome_abi)

# 发送交易函数
def send_transaction(to, value, data, private_key):
    account = Account.from_key(private_key)
    address = account.address
    nonce = web3.eth.get_transaction_count(address, 'pending')

    # Build the EIP-1559 transaction
    tx = {
        'nonce': nonce,
        'to': to,
        'value': value,
        'maxFeePerGas': MAX_BASE_FEE,
        'maxPriorityFeePerGas': PRIORITY_FEE,
        'gas': GAS_LIMIT,
        'data': data,
        'chainId': CHAIN_ID
    }

    try:
        signed_tx = web3.eth.account.sign_transaction(tx, private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)  # Corrected from 'raw_Transaction' to 'raw_transaction'
        return tx_hash
    except Exception as e:
        raise Exception(f"Failed to send transaction: {e}")

# ETH -> WETH 交易
def eth_to_weth(amount, private_key):
    value = amount  # Already in wei
    deposit_function = velodrome_contract.functions.deposit()
    data = deposit_function.build_transaction({
        'value': value,
        'chainId': CHAIN_ID,
        'maxFeePerGas': MAX_BASE_FEE,
        'maxPriorityFeePerGas': PRIORITY_FEE,
        'gas': GAS_LIMIT,
        'nonce': 0  # Placeholder nonce (will be replaced in send_transaction)
    })['data']
    tx_hash = send_transaction(VELODROME_CONTRACT_ADDRESS, value, data, private_key)
    return tx_hash

# WETH -> ETH 交易
def weth_to_eth(amount, private_key):
    value = 0
    withdraw_function = velodrome_contract.functions.withdraw(amount)  # Already in wei
    data = withdraw_function.build_transaction({
        'value': value,
        'chainId': CHAIN_ID,
        'maxFeePerGas': MAX_BASE_FEE,
        'maxPriorityFeePerGas': PRIORITY_FEE,
        'gas': GAS_LIMIT,
        'nonce': 0  # Placeholder nonce (will be replaced in send_transaction)
    })['data']
    tx_hash = send_transaction(VELODROME_CONTRACT_ADDRESS, value, data, private_key)
    return tx_hash

# 主函数
def main():
    # 自定义交易金额和次数
    eth_amount = 0.001  # 每次交易的ETH数量
    num_transactions = 2  # 每个地址的交易次数

    # 加载私钥列表
    with open(PRIVATE_KEY_FILE, 'r') as file:
        private_keys = [line.strip() for line in file.readlines()]

    # 处理每个地址
    for private_key in private_keys:
        account = Account.from_key(private_key)
        address = account.address
        # Check account balance
        balance = web3.eth.get_balance(address)
        balance_eth = web3.from_wei(balance, 'ether')
        print(f"Processing address: {address}, Balance: {balance_eth} ETH")

        # Check if balance is sufficient
        required_eth = eth_amount + (GAS_LIMIT * MAX_BASE_FEE / 10**18)  # ETH amount + max gas cost
        if balance_eth < required_eth:
            print(f"Insufficient funds: Required {required_eth} ETH, but only {balance_eth} ETH available.")
            continue

        for i in range(num_transactions):
            try:
                print(f"Transaction {i+1}: ETH -> WETH")
                wei_amount = web3.to_wei(eth_amount, 'ether')
                tx_hash = eth_to_weth(wei_amount, private_key)
                print(f"Transaction hash: {web3.to_hex(tx_hash)}")
                receipt = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
                if receipt.status == 1:
                    print("ETH -> WETH transaction successful")
                else:
                    print("ETH -> WETH transaction failed")
                time.sleep(10)

                print(f"Transaction {i+1}: WETH -> ETH")
                wei_amount = web3.to_wei(eth_amount, 'ether')
                tx_hash = weth_to_eth(wei_amount, private_key)
                print(f"Transaction hash: {web3.to_hex(tx_hash)}")
                receipt = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
                if receipt.status == 1:
                    print("WETH -> ETH transaction successful")
                else:
                    print("WETH -> ETH transaction failed")
                time.sleep(10)
            except Exception as e:
                print(f"Transaction failed: {e}")
                continue

        sleep_time = random.randint(2, 8)
        print(f"Finished processing address: {address}")
        print(f"Waiting for {sleep_time} seconds before processing the next address...")
        time.sleep(sleep_time)

if __name__ == "__main__":
    main()
