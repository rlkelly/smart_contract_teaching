from typing import Dict, List

from block import Block, GenesisBlock
from transaction import Transaction


class Blockchain(object):
    accounts: Dict[str, int] = {}
    contracts: Dict[str, int] = {}
    blocks: List[Block] = []
    difficulty = '00ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff'

    def __init__(self, creator: str, prev_blocks: List[Block]=None):
        if prev_blocks is None:
            self.prev_blocks = [GenesisBlock()]
        else:
            self.prev_blocks = [prev_blocks]
        self.current_block = Block(creator, self.prev_blocks[-1].block_header_hash)
        self.prev_block = self.prev_blocks[-1]

    def verify_transaction(self, transaction: Transaction) -> bool:
        return transaction.sender in self.accounts and transaction.amount < self.accounts[transaction.sender]

    def verify_block(self) -> bool:
        for transaction in self.current_block.transactions:
            assert transaction.verify()
        assert block.get_merkle_root == block.merkle_root
        assert int(block.get_header_hash(), 16) < int(difficulty, 16)
        return True

    def mine_block(self) -> bool:
        self.current_block.get_merkle_root()
        block_hash = self.current_block.get_header_hash()
        if int(block_hash, 16) < int(self.difficulty, 16):
            # meets difficulty requirement!!
            self.prev_blocks.append(self.current_block)
            self.current_block = Block()
            return True
        return False


def test():
    b = Blockchain('3a1bcfa12a29a7ed68b1c70743a104cc37e6ae8e2c94653fcc1093707a62c448f98ac599df92d392a9f56c2a46bca5a375b9996f321c490b2e92c7c71cf1e134')
    b.mine_block()

if __name__ == '__main__':
    test()