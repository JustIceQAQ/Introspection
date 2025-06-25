def test_aes256_cbc_import():
    from helpers.cryptography.rsa2048 import RSA2048Cipher  # noqa
    from helpers.cryptography.rsa2048.helper import RSA2048Cipher  # noqa


def test_aes256_cbc_encrypter(original_plaintext, a_pair_keys):
    from helpers.cryptography.rsa2048 import RSA2048Cipher
    private_key_pem, public_key_pem = a_pair_keys

    rsa2048_cipher = RSA2048Cipher(public_key_pem, private_key_pem)
    ciphertext = rsa2048_cipher.encrypter(original_plaintext)
    assert ciphertext != original_plaintext


def test_aes256_cbc_decrypter(original_plaintext, a_pair_keys):
    from helpers.cryptography.rsa2048 import RSA2048Cipher
    private_key_pem, public_key_pem = a_pair_keys
    rsa2048_cipher = RSA2048Cipher(public_key_pem, private_key_pem)
    ciphertext = rsa2048_cipher.encrypter(original_plaintext)
    assert ciphertext != original_plaintext
    decrypted_plaintext = rsa2048_cipher.decrypter(ciphertext)
    assert decrypted_plaintext == original_plaintext
