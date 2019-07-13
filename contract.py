from typing import Dict, List
from hashlib import sha256
import json

from opcodes import *


class Transaction(object):
    def __init__(
        self,
        sender,
        receiver,
        amount,
    ):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

    def dumps(self):
        return {
            'from': self.sender,
            'to': self.receiver,
            'amount': self.amount,
        }


class Block(object):
    def __init__(self, prev_block_hash):
        self.nonce = 0
        self.transactions = []
        self.previous_block_hash = prev_block_hash
        self.block_hash = None

    def generate_json_string(self):
        return json.dumps({
            'previous_block_hash': self.previous_block_hash,
            'nonce': self.nonce,
            'transactions': [t.dumps() for t in self.transactions]
        }).encode('utf-8')

    def add_transaction(self, transaction: Transaction):
        self.transactions.append(transaction)

    def increment_nonce(self):
        self.nonce += 1

    def hash(self):
        return sha256(self.generate_json_string()).hexdigest()


class Blockchain(object):
    accounts: Dict[str, int] = {}
    contracts: Dict[str, int] = {}
    blocks: List[Block] = []
    difficulty = '000'

    def __init__(self):
        self.current_block = Block()

    def verify_transaction(self, transaction: Transaction) -> bool:
        return transaction.sender in self.accounts and transaction.amount < self.accounts[transaction.sender]

    def verify_block(self) -> bool:
        for transaction in self.current_block.transactions:
            if self.sender not in accounts or accounts[self.sender] < self.amount:
                return False
        return True

    def mine_block(self):
        block_hash = self.current_block.hash()
        if block_hash[:len(difficulty)] != difficulty:
            return False
        return True


class SmartContract(object):
    OPCODES = {
        'PUSH': push,
        'POP': pop,
        'SWAP': swap,
        'ADD': add,
        'SUB': sub,
        'MUL': mul,
        'DIV': div,
        'MOD': mod,
        'GREATER': is_greater,
        'STORAGE': store,
    }

    # the stack has a maximum size of 1024
    def __init__(contract, balance: int, code: str, storage: dict):
        contract.balance = balance
        contract.code = code

        contract.stack = Stack(contract)
        contract.storage = storage
        contract.memory = {}

        contract.gas_balance = 0

    def update_storage(contract, key, value):
        contract.storage[key] = value
        return value

    def delete_memory(contract):
        contract.memory = {}

    def return_leftover_gas(contract):
        pass

    def execute(contract, gas_balance, args: dict):
        contract.gas_balance = gas_balance
        contract.memory = args
        contract.stack = Stack(contract)

        contract.delete_memory()


if __name__ == '__main__':
    code = '''
        PUSH 10
        PUSH 20
    '''
