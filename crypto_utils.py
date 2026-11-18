
import hashlib

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding


# SHA-256 Hash Generation
def calculate_hash(file_data):
    return hashlib.sha256(file_data).hexdigest()


# Load Private Key
def load_private_key():
    with open("keys/private_key.pem", "rb") as file:
        private_key = serialization.load_pem_private_key(
            file.read(),
            password=None
        )
    return private_key


# Load Public Key
def load_public_key():
    with open("keys/public_key.pem", "rb") as file:
        public_key = serialization.load_pem_public_key(
            file.read()
        )
    return public_key


# Generate Digital Signature
def sign_file(file_data):

    private_key = load_private_key()

    digital_signature = private_key.sign(
        file_data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    return digital_signature


# Verify Digital Signature
def verify_file(file_data, digital_signature):

    public_key = load_public_key()

    try:
        public_key.verify(
            digital_signature,
            file_data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        return True

    except Exception:
        return False
