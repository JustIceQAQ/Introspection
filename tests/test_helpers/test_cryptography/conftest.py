import secrets

import pytest

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


@pytest.fixture(scope='function')
def original_plaintext():
    return secrets.token_hex(16)


@pytest.fixture(scope='function')
def key():
    return secrets.token_hex(16)


@pytest.fixture(scope='function')
def iv():
    return secrets.token_hex(8)


@pytest.fixture(scope="function")
def a_pair_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_key = private_key.public_key()
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return private_key_pem, public_key_pem
