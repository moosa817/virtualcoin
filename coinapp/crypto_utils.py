# crypto_utils.py

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import (
    load_pem_private_key,
)
from cryptography.exceptions import InvalidSignature
import base64
from cryptography.hazmat.primitives.serialization import load_pem_public_key

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa


def generate_rsa_keypair():
    """
    Generates an RSA key pair (public key and private key).

    Returns:
        private_key_pem (str): RSA private key encoded as PEM format string.
        public_key_pem (str): RSA public key encoded as PEM format string.
    """
    # Generate RSA key pair
    private_key = rsa.generate_private_key(
        public_exponent=65537, key_size=2048, backend=default_backend()
    )

    # Get the public key in PEM format
    public_key_pem = (
        private_key.public_key()
        .public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        .decode()
    )

    # Get the private key in PEM format
    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode()

    return private_key_pem, public_key_pem


def sign_data(data: bytes, private_key_pem: str) -> str:
    """
    Signs data using an RSA private key.

    Args:
        data (bytes): Data to sign.
        private_key_pem (str): RSA private key encoded as PEM format string.

    Returns:
        str: Base64 encoded signature of the data.
    """
    # Load private key from PEM format

    private_key = load_pem_private_key(
        private_key_pem.encode(), password=None, backend=default_backend()
    )

    # Sign the data
    signature = private_key.sign(
        data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256(),
    )

    # Encode the signature in base64
    signature_base64 = base64.b64encode(signature).decode("utf-8")
    return signature_base64


def verify_signature(data: bytes, base64_signature: str, public_key_pem: str) -> bool:
    """
    Verifies the signature of data using an RSA public key.

    Args:
        data (bytes): Original data.
        base64_signature (str): Base64 encoded signature to verify.
        public_key_pem (str): RSA public key encoded as PEM format string.

    Returns:
        bool: True if the signature is valid, False otherwise.
    """

    # Decode the base64 encoded signature
    signature = base64.b64decode(base64_signature)

    # Load public key from PEM format
    public_key_obj = load_pem_public_key(
        public_key_pem.encode(), backend=default_backend()
    )

    try:
        # Verify the signature
        public_key_obj.verify(
            signature,
            data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256(),
        )
        return True
    except (InvalidSignature, ValueError):
        return False
