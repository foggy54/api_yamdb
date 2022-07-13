import hashlib
from api_yamdb.settings import SECRET_KEY


def salted_hash(value):
    """Return sha256 salted with SECRET_KEY"""
    salted_value = value + SECRET_KEY
    result = hashlib.sha256(salted_value.encode())
    return result.hexdigest()
