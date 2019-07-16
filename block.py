from hashlib import sha256
import json
import pickle
import time

from transaction import Coinbase, Transaction, generate_test_transaction


class Block(object):
    def __init__(self, creator: str, prev_block_header_hash: bytes=None):
        self.nonce = 0
        self.transactions = [Coinbase(creator)]
        self.previous_block_header_hash = prev_block_header_hash
        self.time = bytes(int(time.time()))
        self.block_header_hash = None
        self.merkle_root = None
        self.header_hash = None

    def add_transaction(self, transaction: Transaction):
        self.transactions.append(transaction)
        self.header_hash = None
        self.merkle_root = None

    def increment_nonce(self):
        self.nonce += 1

    def set_time(self, current_time: bytes):
        self.time = current_time

    def get_header_hash(self):
        m = sha256()
        m.update(self.merkle_root)
        m.update(self.time)
        m.update(self.previous_block_header_hash)
        m.update(bytes(self.nonce))
        self.header_hash = m.digest().hex()
        return self.header_hash

    def get_merkle_root(self):
        # This is a simple implementation of finding the merkle root for the transactions
        transaction_strings = list(sorted([t.dumps() for t in self.transactions]))
        if len(transaction_strings) % 2 != 0:
            transaction_strings.append(b'')
        while True:
            temp = []
            for i in range(0, len(transaction_strings), 2):
                transaction_strings[i]
                transaction_strings[i + 1]
                m = sha256()
                m.update(transaction_strings[i] + transaction_strings[i + 1])
                temp.append(m.digest())
            transaction_strings = temp
            temp = []
            if len(transaction_strings) == 1: break
        self.merkle_root = transaction_strings[0]
        return self.merkle_root

    def dumps(self):
        return pickle.dumps(self)

    @staticmethod
    def loads(data):
        return pickle.loads(data)

class GenesisBlock(Block):
    def __init__(self):
        super(GenesisBlock, self).__init__(b'Noone', b'Nothing')
        self.block_header_hash = b'fafa'

    def get_merkle_root(self):
        self.merkle_root = b'this is the beginning'
        return self.merkle_root


def test():
    t = generate_test_transaction(random=False)
    b = Block('3a1bcfa12a29a7ed68b1c70743a104cc37e6ae8e2c94653fcc1093707a62c448f98ac599df92d392a9f56c2a46bca5a375b9996f321c490b2e92c7c71cf1e134', b'')
    b.add_transaction(t)
    b.get_merkle_root()
    b.set_time(b'10000000')
    assert b.get_header_hash() == '66133b9317522b44b4a0acce652b8efb561b0e892f7a1b0e4ba603848f3f2ac1'
    c = b.dumps()
    b = Block.loads(c)
    assert b.get_header_hash() == '66133b9317522b44b4a0acce652b8efb561b0e892f7a1b0e4ba603848f3f2ac1'

    gb = GenesisBlock()
    gb.get_merkle_root()
    gb.get_header_hash()


if __name__ == '__main__':
    test()
