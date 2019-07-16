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
        'SSTORE': sstore,
        'SLOAD': sload,
        'MSTORE': mstore,
        'MLOAD': mload,
        'SENDER': sender,
        'AMOUNT': amount,
        'EQUALS': is_equal,
        'BALANCE': balance,
        'TRANSFER': transfer,
        'UNIT': unit,
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

    def update_memory(contract, key, value):
        contract.memory[key] = value
        return value

    def delete_memory(contract):
        contract.memory = {}

    def send_amount(contract, amount: int, receiver: str):
        if contract.balance < int(amount):
            raise Exception('Invalid Balance')
        contract.balance -= int(amount)
        # TODO: Update blockchain

    def return_leftover_gas(contract):
        pass

    def execute(contract, gas_balance, sent_amount: int, sender: str, args: dict={}):
        contract.gas_balance = gas_balance
        contract.sent_amount = sent_amount
        contract.sender = sender
        contract.memory = args
        contract.stack = Stack(contract)

        code = contract.code.strip().split('\n')
        for row in code:
            contract.gas_balance -= 1
            if contract.gas_balance < 0:
                raise Exception('Ran out of gas')
            values = row.strip().split(' ')
            # control flow for IF
            if values[0] == 'IF':
                top = contract.stack.pop()
                if top == '0':
                    values[3:]
                else:
                    values = values[1:]
            contract.OPCODES[values[0]](contract.stack, *values[1:])
            print(contract.stack)

        contract.delete_memory()


if __name__ == '__main__':
    code = '''
        SLOAD magic_word
        MLOAD magic_word
        EQUALS
        SENDER
        SWAP
        BALANCE
        SWAP
        IF TRANSFER ELSE UNIT
    '''
    s = SmartContract(33, code, {'magic_word': 'boo'})
    s.execute(100, 10, 'fafafafa', {'magic_word': 'boo'})
