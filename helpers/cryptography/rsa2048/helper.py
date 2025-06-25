import base64
from typing import Callable
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from ..base import CipherBase

__all__ = {
    "RSA2048Cipher"
}


class RSA2048Cipher(CipherBase):
    """基於 RSA 2048 SHA256 MGF1 的加解密元件 (未實作簽驗章功能)"""

    _hashes = hashes.SHA256
    _mgf = padding.MGF1

    def __init__(
            self,
            public_key_pem: bytes | None = None,
            private_key_pem: bytes | None = None,
    ):
        self.public_key = (
            serialization.load_pem_public_key(public_key_pem, backend=default_backend())
            if public_key_pem
            else None
        )

        self.private_key = (
            serialization.load_pem_private_key(
                private_key_pem,
                password=None,
            )
            if private_key_pem
            else None
        )

    def _encrypter(self, plaintext: str | bytes) -> str:
        runtime_plaintext = (
            plaintext.encode("utf-8") if isinstance(plaintext, str) else plaintext
        )
        ciphertext = self.public_key.encrypt(
            runtime_plaintext,
            padding.OAEP(
                mgf=self._mgf(algorithm=self._hashes()),
                algorithm=self._hashes(),
                label=None,
            ),
        )
        return base64.b64encode(ciphertext).decode()

    def encrypter(
            self, plaintext: str | bytes, auto_error: bool = True
    ) -> str | None:
        if self.public_key is None:
            raise ValueError("You not set public_key")

        return (
            self._encrypter(plaintext)
            if auto_error
            else self._try_error_protect(self._encrypter, plaintext)
        )

    def _decrypter(self, ciphertext: str | bytes) -> str:
        runtime_ciphertext = base64.b64decode(ciphertext)
        return self.private_key.decrypt(
            runtime_ciphertext,
            padding.OAEP(
                mgf=self._mgf(algorithm=self._hashes()),
                algorithm=self._hashes(),
                label=None,
            ),
        ).decode()

    def decrypter(
            self, ciphertext: str | bytes, auto_error: bool = True
    ) -> str | None:
        if self.private_key is None:
            raise ValueError("You not set private_key")
        return (
            self._decrypter(ciphertext)
            if auto_error
            else self._try_error_protect(self._decrypter, ciphertext)
        )

    def _try_error_protect(self, method: Callable, text: str | bytes) -> str | None:
        result_text = None
        try:
            result_text = method(text)
        except Exception:  # nosec B110
            pass

        return result_text

    def _signer(self, message: str | bytes) -> str:
        if not self.private_key:
            raise ValueError("You not set private_key")
        runtime_msg = message.encode("utf-8") if isinstance(message, str) else message
        signature = self.private_key.sign(
            runtime_msg,
            padding.PSS(
                mgf=self._mgf(self._hashes()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            self._hashes(),
        )
        return base64.b64encode(signature).decode()

    def signer(self, message: str | bytes, auto_error: bool = True) -> str | None:
        return (
            self._signer(message)
            if auto_error
            else self._try_error_protect(self._signer, message)
        )

    def _verifier(self, message: str | bytes, signature: str | bytes) -> bool:
        if not self.public_key:
            raise ValueError("You not set public_key")
        runtime_msg = message.encode("utf-8") if isinstance(message, str) else message
        runtime_sig = (
            base64.b64decode(signature) if isinstance(signature, str) else signature
        )

        self.public_key.verify(
            runtime_sig,
            runtime_msg,
            padding.PSS(
                mgf=self._mgf(self._hashes()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            self._hashes(),
        )
        return True

    def verifier(
            self, message: str | bytes, signature: str | bytes, auto_error: bool = True
    ) -> bool:
        def safe_verify(msg_sig):
            try:
                return self._verifier(*msg_sig)
            except Exception:  # nosec
                return False

        return (
            self._verifier(message, signature)
            if auto_error
            else safe_verify((message, signature))
        )
