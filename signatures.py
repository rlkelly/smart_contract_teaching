import binascii

import ecdsa


def generate_keypair():
    sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
    vk = sk.get_verifying_key()
    return sk.to_string().hex(), vk.to_string().hex()


def sign_message(message, sk_string):
    try:
        sk_bytes = binascii.unhexlify(sk_string)
        sk = ecdsa.SigningKey.from_string(sk_bytes, curve=ecdsa.SECP256k1)
    except:
        raise Exception('Invalid Signing Key.  Try again with Hex!')
    sig = sk.sign(message)
    return sig.hex()


def verify(message, sig, vk_string):
    vk_bytes = binascii.unhexlify(vk_string)
    vk = ecdsa.VerifyingKey.from_string(vk_bytes, curve=ecdsa.SECP256k1)
    sig_bytes = binascii.unhexlify(sig)
    try:
        # Good Signature
        return vk.verify(sig_bytes, message) # True
    except ecdsa.keys.BadSignatureError:
        # Bad Signature
        return False


def test():
    sk, vk = generate_keypair()
    sig = sign_message(b'test', sk)
    assert verify(b'test', sig, vk) == True
    print('Tests Passed')


if __name__ == '__main__':
    test()
