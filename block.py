from __future__ import annotations

import binascii
from hashlib import sha256
import json
import pickle
import time

from transaction import Coinbase, Transaction, generate_test_transaction


class Block(object):
    def __init__(self, creator: str, prev_block_header_hash: bytes=None):
        self.creator = creator
        self.nonce = 0
        self.transactions = [Coinbase(creator)]
        self.previous_block_header_hash = prev_block_header_hash
        self.time = bytes(int(time.time()))
        self.block_header_hash = None
        self.merkle_root = None

    def _reset_header_hashes(self):
        self.block_header_hash = None
        self.merkle_root = None

    def add_transaction(self, transaction: Transaction):
        self.transactions.append(transaction)
        self._reset_header_hashes()

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
        self.block_header_hash = m.digest()
        return self.block_header_hash

    def get_merkle_root(self) -> bytes:
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

    def verify_transactions(self):
        for transaction in self.transactions:
            assert transaction.verify()

    @staticmethod
    def loads(data) -> Block:
        data = json.loads(data)
        b =  Block(
            creator=data['creator'],
            prev_block_header_hash= binascii.unhexlify(data['previous_block_header_hash']),
        )
        b.transactions = [Transaction.loads(binascii.unhexlify(t)) for t in data['transactions']]
        b.time = binascii.unhexlify(data['time'])
        b.block_header_hash = data['block_header_hash']
        b.merkle_root = binascii.unhexlify(data['merkle_root'])
        b.nonce = data['nonce']
        return b

    def dumps(self) -> str:
        return json.dumps({
            'creator': self.creator,
            'nonce': self.nonce,
            'transactions': [t.dumps(with_sig=True).hex() for t in self.transactions],
            'previous_block_header_hash':  self.previous_block_header_hash.hex(),
            'time': self.time.hex(),
            'block_header_hash': self.block_header_hash.hex(),
            'merkle_root': self.merkle_root.hex(),
        }).encode('utf-8')


class GenesisBlock(Block):
    def __init__(self):
        super(GenesisBlock, self).__init__('Noone', b'Nothing')
        self.block_header_hash = b'fafa'

    def get_merkle_root(self):
        self.merkle_root = b'this is the beginning'
        return self.merkle_root


def test():
    t = generate_test_transaction(random=False)
    b = Block('3a1bcfa12a29a7ed68b1c70743a104cc37e6ae8e2c94653fcc1093707a62c448f98ac599df92d392a9f56c2a46bca5a375b9996f321c490b2e92c7c71cf1e134', b'')
    b.add_transaction(t)
    b.set_time(b'10000000')
    b.get_merkle_root()
    assert b.get_header_hash().hex() == '24d5e60a7877a34527afefbb2e05c7940789f3c75dc783f23f85b81336c0881d'
    c = b.dumps()
    b = Block.loads(c)
    assert b.get_header_hash().hex() == '24d5e60a7877a34527afefbb2e05c7940789f3c75dc783f23f85b81336c0881d'

    gb = GenesisBlock()
    gb.get_merkle_root()
    gb.get_header_hash()


if __name__ == '__main__':
    test()
