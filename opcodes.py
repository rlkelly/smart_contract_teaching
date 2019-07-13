class Stack(object):
    def __init__(self, contract):
        self.stack = []
        self.contract = contract

    def pop(self):
        return self.pop(-1)

    def push(self, value):
        stack.append(value)

class Pair(object):
    def __init__(self, left, right):
        self.left = left
        self.right = right

def push(stack: Stack, *args):
    elem = args[0]
    stack.push(elem)

def pop(stack: Stack, *args):
    return stack.pop()

def add(stack: Stack, *args):
    x = stack.pop()
    y = stack.pop()
    return x + y

def sub(stack: Stack, *args):
    x = stack.pop()
    y = stack.pop()
    return x - y

def mul(stack: Stack, *args):
    x = stack.pop()
    y = stack.pop()
    return x * y

def div(stack: Stack, *args):
    x = stack.pop()
    y = stack.pop()
    return x // y

def mod(stack: Stack, *args):
    x = stack.pop()
    y = stack.pop()
    return x % y

def is_greater(stack: Stack, *args):
    x = stack.pop()
    y = stack.pop()
    return x > y

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

def store(stack: Stack, *args):
    key: str = args[0]
    value = args[1]
    self.contract.update_storage(key, value)

# SLOAD
# SSTORE
