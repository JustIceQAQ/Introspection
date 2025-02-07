import secrets

import pytest


@pytest.fixture(scope='function')
def original_plaintext():
    return secrets.token_hex(16)


@pytest.fixture(scope='function')
def key():
    return secrets.token_hex(16)


@pytest.fixture(scope='function')
def iv():
    return secrets.token_hex(8)
