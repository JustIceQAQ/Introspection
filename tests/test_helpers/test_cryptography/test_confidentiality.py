import base64
import json

from helpers.cryptography.aes256_cbc import AES256Cipher
from helpers.cryptography.rsa2048 import RSA2048Cipher


def test_confidentiality(original_plaintext, key, iv, a_pair_keys):
    private_key_pem_a, public_key_pem_a = a_pair_keys
    data = {
        "QAQ": original_plaintext,
    }
    base64_data = base64.b64encode(json.dumps(data).encode()).decode()
    aes256_cipher = AES256Cipher(key, iv)
    encrypter_data = aes256_cipher.encrypter(base64_data)

    rsa2048_cipher = RSA2048Cipher(public_key_pem_a, private_key_pem_a)
    encrypter_keyiv = rsa2048_cipher.encrypter(aes256_cipher.key + aes256_cipher.iv)

    ##

    rsa2048_cipher2 = RSA2048Cipher(public_key_pem_a, private_key_pem_a)
    decrypter_keyiv = rsa2048_cipher2.decrypter(encrypter_keyiv)

    assert decrypter_keyiv == aes256_cipher.key + aes256_cipher.iv
    decrypter_key = decrypter_keyiv[:32]
    decrypter_iv = decrypter_keyiv[32:]
    assert decrypter_key == aes256_cipher.key
    assert decrypter_iv == aes256_cipher.iv

    aes256_cipher2 = AES256Cipher(key, iv)
    decrypter_data = aes256_cipher2.decrypter(encrypter_data)
    assert decrypter_data == base64_data

    loads_data = json.loads(base64.b64decode(decrypter_data))
    assert loads_data["QAQ"] == data["QAQ"]
