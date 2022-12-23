from cryptography.hazmat.primitives.asymmetric import rsa

# https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/
if __name__ == '__main__':
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public_key = private_key.public_key()

    message = b"encrypted data"
