from typing import Dict, List
from hashlib import sha256
import json
import time

from opcodes import *
from signatures import *
from transaction import Transaction


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
