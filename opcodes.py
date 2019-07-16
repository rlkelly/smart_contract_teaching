class Stack(object):
    def __init__(self, contract):
        self.stack = []
        self.contract = contract

    def pop(self):
        return self.stack.pop(-1)

    def push(self, value):
        self.stack.append(value)

    def __repr__(self):
        return '----------------\n' + '\n'.join(self.stack[::-1]) + '\n----------------\n'

def push(stack: Stack, *args):
    elem = args[0] # String or Int
    stack.push(elem)

def pop(stack: Stack, *args):
    return stack.pop()

def add(stack: Stack, *args):
    x = stack.pop()
    y = stack.pop()
    stack.push(x + y)

def sub(stack: Stack, *args):
    x = stack.pop()
    y = stack.pop()
    stack.push(x - y)

def mul(stack: Stack, *args):
    x = stack.pop()
    y = stack.pop()
    stack.push(x * y)

def div(stack: Stack, *args):
    x = stack.pop()
    y = stack.pop()
    stack.push(x // y)

def mod(stack: Stack, *args):
    x = stack.pop()
    y = stack.pop()
    stack.push(x % y)

def is_equal(stack: Stack, *args):
    x = stack.pop()
    y = stack.pop()
    if x == y:
        stack.push('1')
    else:
        stack.push('0')

def is_greater(stack: Stack, *args):
    x = stack.pop()
    y = stack.pop()
    if x > y:
        stack.push('1')
    else:
        stack.push('0')

def concat(stack: Stack, *args):
    x = stack.pop()
    y = stack.pop()
    assert type(x) == type(y) == str
    stack.push(f'{x}{y}')

def swap(stack: Stack, *args):
    x = stack.pop()
    y = stack.pop()
    stack.push(x)
    stack.push(y)

def sstore(stack: Stack, *args):
    key: str = args[0]
    value = args[1]
    stack.contract.update_storage(key, value)

def sload(stack: Stack, *args):
    key: str = args[0]
    stack.push(stack.contract.storage[key])

def mstore(stack: Stack, *args):
    key: str = args[0]
    value = args[1]
    stack.contract.update_memory(key, value)

def mload(stack: Stack, *args):
    print(stack.contract.memory)
    key: str = args[0]
    stack.push(stack.contract.memory[key])

def sender(stack: Stack, *args):
    stack.push(stack.contract.sender)

def amount(stack: Stack, *args):
    sender = sel
    stack.push(stack.contract.amount)

def balance(stack: Stack, *args):
    stack.push(str(stack.contract.balance))

def transfer(stack: Stack, *args):
    amount = stack.pop()
    receiver = stack.pop()
    stack.contract.send_amount(amount, receiver)

def unit(stack: Stack, *args):
    pass

# TODO: add mapping functions
