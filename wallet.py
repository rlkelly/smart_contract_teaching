import binascii

import ecdsa

from transaction import Transaction
from signatures import generate_keypair


class Wallet(object):
    def __init__(self, private_key=None):
        if private_key == None:
            self.private_key, self.public_key = generate_keypair()
        else:
            sk_bytes = binascii.unhexlify(private_key)
            sk = ecdsa.SigningKey.from_string(sk_bytes, curve=ecdsa.SECP256k1)
            self.private_key = private_key
            self.public_key = sk.get_verifying_key().to_string().hex()

    def create_transaction(self, receiver: str, amount: int):
        t = Transaction(sender=self.public_key, receiver=receiver, amount=amount)


def test():
    w = Wallet()
    w.create_transaction('956007d275b58c2327edc95c11a27c7ff9819472ca81cf24f51ee1ace831867709b097c3bf5f0e26cb3efa342e5676d07674368fedaac5784f95b12415fddc3c', 10)
    w = Wallet('bef350a707c071aeca83c579d40829930d4aea196b29b4620459a8184e39d9cf')
    w.create_transaction('956007d275b58c2327edc95c11a27c7ff9819472ca81cf24f51ee1ace831867709b097c3bf5f0e26cb3efa342e5676d07674368fedaac5784f95b12415fddc3c', 10)


if __name__ == '__main__':
    test()
