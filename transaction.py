from __future__ import annotations

import binascii
import json

from signatures import generate_keypair, sign_message, verify


class Transaction(object):
    def __init__(
        self,
        sender: str,
        receiver: str,
        amount: int,
        signature: string='',
    ):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.signature = signature

    def verify(self) -> bool:
        try:
            assert self.signature != ''
            assert verify(self.dumps(), self.signature, self.sender)
            return True
        except:
            return False

    def sign(self, private_key: str) -> str:
        self.signature = sign_message(self.dumps(), private_key)
        return self.signature

    @staticmethod
    def loads(data) -> Transaction:
        data = json.loads(data)
        if 'signature' in data:
            data['signature'] = binascii.unhexlify(data['signature'])
        return Transaction(**data)

    def dumps(self, with_sig: bool=False) -> bytes:
        if with_sig:
            return json.dumps({
                'sender': self.sender,
                'receiver': self.receiver,
                'amount': self.amount,
                'signature': self.signature,
            }).encode('utf-8')
        return json.dumps({
            'sender': self.sender,
            'receiver': self.receiver,
            'amount': self.amount,
        }).encode('utf-8')


class Coinbase(Transaction):
    def __init__(self, receiver: str):
        super(Coinbase, self).__init__('0000', receiver, 1)

    def verify(self) -> bool:
        return True

    def sign(self, private_key: str):
        pass


def generate_test_transaction(random=True):
    if not random:
        sender_private_key = 'bef350a707c071aeca83c579d40829930d4aea196b29b4620459a8184e39d9cf'
        sender_public_key = '3a1bcfa12a29a7ed68b1c70743a104cc37e6ae8e2c94653fcc1093707a62c448f98ac599df92d392a9f56c2a46bca5a375b9996f321c490b2e92c7c71cf1e134'
        receiver_public_key = '956007d275b58c2327edc95c11a27c7ff9819472ca81cf24f51ee1ace831867709b097c3bf5f0e26cb3efa342e5676d07674368fedaac5784f95b12415fddc3c'
    else:
        sender_private_key, sender_public_key = generate_keypair()
        _, receiver_public_key = generate_keypair()
    t = Transaction(
        sender=sender_public_key,
        receiver=receiver_public_key,
        amount=1,
    )
    t.sign(sender_private_key)
    return t


def test_verify():
    sender_private_key, sender_public_key = generate_keypair()
    receiver_private_key, receiver_public_key = generate_keypair()
    t = Transaction(
        sender=sender_public_key,
        receiver=receiver_public_key,
        amount=1,
    )
    t.sign(sender_private_key)
    assert t.verify()

    t.sign(receiver_private_key)
    assert not t.verify()

    t = generate_test_transaction()
    assert t.verify()
    t = generate_test_transaction(random=False)
    assert t.verify()


def test_coinbase():
    c = Coinbase('3a1bcfa12a29a7ed68b1c70743a104cc37e6ae8e2c94653fcc1093707a62c448f98ac599df92d392a9f56c2a46bca5a375b9996f321c490b2e92c7c71cf1e134')
    c.sign('')
    assert c.verify()


if __name__ == '__main__':
    test_verify()
    test_coinbase()
