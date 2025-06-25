import json

from helpers.cryptography.rsa2048 import RSA2048Cipher


def test_integrity(original_plaintext, key, iv, a_pair_keys):
    private_key_pem_a, public_key_pem_a = a_pair_keys
    data = {
        "QAQ": original_plaintext,
    }

    dumps_data = json.dumps(data)
    rsa2048_cipher = RSA2048Cipher(public_key_pem_a, private_key_pem_a)

    signer_token = rsa2048_cipher.signer(dumps_data)

    rsa2048_cipher2 = RSA2048Cipher(public_key_pem_a, private_key_pem_a)


    assert rsa2048_cipher2.verifier(dumps_data, signer_token) is True


