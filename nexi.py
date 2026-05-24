import os

__version__ = "1.0.0"

def nexi(data: bytes, key: bytes) -> bytes:
    out = bytearray()
    for i, b in enumerate(data):
        k = key[i % 4]
        out.append((b + k) & 0xFF)
    return bytes(out)

def nexi_decrypt(data: bytes, key: bytes) -> bytes:
    out = bytearray()
    for i, b in enumerate(data):
        k = key[i % 4]
        out.append((b - k) & 0xFF)
    return bytes(out)

def nextxi_ori(data, key=None, decrypt=False):
    if isinstance(data, str):
        data = data.encode("utf-8")

    if key is None:
        key = os.urandom(16)

    if decrypt:
        return nexi_decrypt(data, key)
    else:
        return nexi(data, key)