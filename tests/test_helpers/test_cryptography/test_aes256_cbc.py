def test_aes256_cbc_import():
    from helpers.cryptography.aes256_cbc import AES256Cipher  # noqa
    from helpers.cryptography.aes256_cbc.helper import AES256Cipher  # noqa


def test_aes256_cbc_encrypter(original_plaintext, key, iv):
    from helpers.cryptography.aes256_cbc import AES256Cipher
    aes256_cipher = AES256Cipher(key, iv)
    ciphertext = aes256_cipher.encrypter(original_plaintext)
    assert ciphertext != original_plaintext


def test_aes256_cbc_decrypter(original_plaintext, key, iv):
    from helpers.cryptography.aes256_cbc import AES256Cipher
    aes256_cipher = AES256Cipher(key, iv)
    ciphertext = aes256_cipher.encrypter(original_plaintext)
    assert ciphertext != original_plaintext
    decrypted_plaintext = aes256_cipher.decrypter(ciphertext)
    assert decrypted_plaintext == original_plaintext
