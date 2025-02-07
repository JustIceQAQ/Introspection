from ..base import CipherBase
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import codecs

class ASE256Cipher(CipherBase):
    _algorithms = algorithms.AES256
    _modes = modes.CBC
    _block_size = 16
    _encoding = "utf-8"

    def __init__(self, key: str, iv: str):
        self._key: bytes = key.encode(self._encoding)
        self._iv: bytes = iv.encode(self._encoding)
        self._cipher = Cipher(self._algorithms(self._key), self._modes(self._iv))

    def _padding(self, plaintext: str) -> str:
        pad_string = (self._block_size - len(plaintext) % self._block_size) * chr(
            self._block_size - len(plaintext) % self._block_size)
        return plaintext + pad_string

    def _unpadding(self, plaintext) -> bytes:
        return plaintext[: -ord(plaintext[len(plaintext) - 1:])]

    def encrypter(self, plaintext: str) -> str:
        encryptor = self._cipher.encryptor()
        padded_plaintext = self._padding(plaintext)
        ciphertext = encryptor.update(padded_plaintext.encode(self._encoding)) + encryptor.finalize()
        return codecs.encode(ciphertext, "base64").decode().strip()

    def decrypter(self, ciphertext: str) -> str:
        decrypt = self._cipher.decryptor()
        ciphertext_encoded = codecs.decode(ciphertext.encode(self._encoding), "base64")
        plaintext = decrypt.update(ciphertext_encoded) + decrypt.finalize()
        plaintext_unpadding = self._unpadding(plaintext)
        return plaintext_unpadding.decode()
