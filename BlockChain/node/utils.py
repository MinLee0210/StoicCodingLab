from Crypto.Hash import SHA256

def calculate_hash(data: bytes) -> str:
    hash_obj = SHA256.new()
    hash_obj.update(data)
    return hash_obj.hexdigest