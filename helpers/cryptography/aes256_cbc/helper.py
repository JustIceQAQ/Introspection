import base64
from typing import Callable
from ..base import CipherBase
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as primitives_padding

__all__ = {
    "AES256Cipher"
}

StrOrBytes = str | bytes


class AES256Cipher(CipherBase):
    """基於 AES256 CBC 的加解密元件"""

    _algorithms = algorithms.AES256
    _modes = modes.CBC
    _block_size = 16 * 8  # bit
    _padding = primitives_padding.PKCS7

    def __init__(
            self,
            key: StrOrBytes,
            iv: StrOrBytes,
            use_urlsafe: bool | None = True,
    ):
        self.key = key
        self.iv = iv
        self._key: bytes = self._get_key(key)
        self._iv: bytes = self._get_iv(iv)
        self._base64_encode = (
            base64.urlsafe_b64encode if use_urlsafe else base64.b64encode
        )
        self._base64_decode = (
            base64.urlsafe_b64decode if use_urlsafe else base64.b64decode
        )

    def _get_cipher(self) -> Cipher:
        return Cipher(self._algorithms(self._key), self._modes(self._iv))

    def _get_key(self, runtime_key: StrOrBytes) -> bytes:
        return (
            runtime_key
            if isinstance(runtime_key, bytes)
            else runtime_key.encode(self._encoding)
        )

    def _get_iv(self, runtime_iv: StrOrBytes) -> bytes:
        return (
            runtime_iv
            if isinstance(runtime_iv, bytes)
            else runtime_iv.encode(self._encoding)
        )

    def _encrypter(
            self, data: StrOrBytes, return_type: CipherBase.ReturnType
    ) -> StrOrBytes:
        """:param data: 需要加密的資料"""

        runtime_plaintext = (
            data if isinstance(data, bytes) else data.encode(self._encoding)
        )

        # 依照 block size 設定，來補足相應的bit
        padder = self._padding(self._block_size).padder()
        padded_data = padder.update(runtime_plaintext) + padder.finalize()

        # 載入加密模式
        encrypter = self._get_cipher().encryptor()
        ciphertext = encrypter.update(padded_data) + encrypter.finalize()

        # bytes 轉 base64 (urlsafe)
        if return_type in {CipherBase.ReturnType.Str}:
            return self._base64_encode(ciphertext).decode()
        else:
            return ciphertext

    def encrypter(
            self,
            plaintext: StrOrBytes,
            auto_error: bool | None = True,
            return_type: CipherBase.ReturnType = CipherBase.ReturnType.Str,
    ) -> StrOrBytes:
        """
        :param plaintext: 需要加密的資料
        :param auto_error: True: raise except ; False: return None
        :param return_type:
        """
        return (
            self._encrypter(plaintext, return_type)
            if auto_error
            else self._try_error_protect(self._encrypter, plaintext, return_type)
        )

    def _decrypter(
            self, ciphertext: StrOrBytes, return_type: CipherBase.ReturnType
    ) -> StrOrBytes:
        """
        :param ciphertext: 需要解密的密文
        :param auto_error:
        :param return_type:
        """
        # 載入解密模式
        decrypter = self._get_cipher().decryptor()

        runtime_ciphertext = (
            ciphertext
            if isinstance(ciphertext, bytes)
            else ciphertext.encode(self._encoding)
        )

        # base64 (urlsafe) 轉 bytes
        ciphertext_encoded = self._base64_decode(runtime_ciphertext)
        plaintext_padded_data = decrypter.update(ciphertext_encoded) + decrypter.finalize()

        # 載入字串填充處理
        unpadder = self._padding(self._block_size).unpadder()
        plaintext = unpadder.update(plaintext_padded_data)
        plaintext += unpadder.finalize()

        if return_type in {CipherBase.ReturnType.Str}:
            return plaintext.decode()
        else:
            return plaintext

    def decrypter(
            self,
            ciphertext: StrOrBytes,
            auto_error: bool = True,
            return_type: CipherBase.ReturnType = CipherBase.ReturnType.Str,
    ) -> StrOrBytes:
        return (
            self._decrypter(ciphertext, return_type)
            if auto_error
            else self._try_error_protect(self._decrypter, ciphertext, return_type)
        )

    def _try_error_protect(
            self, method: Callable, text: StrOrBytes, return_type: CipherBase.ReturnType
    ) -> str | None:
        result_text = None
        try:
            result_text = method(text, return_type)
        except Exception:  # nosec B110
            pass

        return result_text
