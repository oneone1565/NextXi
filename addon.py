import hashlib
import os
from typing import Optional
from nexi import nexi, nexi_decrypt

__version__ = "2.0.0"

# ===== Nesh 扩展 =====
def nesh(data: bytes) -> bytes:
    h = hashlib.blake2b()
    h.update(data)
    return h.digest()

def nextxi_with_nesh(data: bytes, key: bytes) -> bytes:
    base = nesh(data, key)  # Nesh 只是参与
    out = bytearray()
    for i, b in enumerate(data):
        k = key[i % 4]
        out.append((b + k) & 0xFF)
    return bytes(out)


def nextxi_with_nesh_decrypt(data: bytes, key: bytes) -> bytes:
    base = nesh(data, key)
    out = bytearray()
    for i, b in enumerate(data):
        k = key[i % 4]
        out.append((b - k) & 0xFF)
    return bytes(out)

def nextxi(
    data,
    key: Optional[bytes] = None,
    use_nesh: bool = True
):
    # 加密
    if isinstance(data, str):
        if key is None:
            key = os.urandom(16)
        data = data.encode("utf-8")
        if use_nesh:
            return nexi_with_nesh(data, key)
        else:
            return nexi(data, key)

    # 解密
    if isinstance(data, bytes):
        if key is None:
            raise ValueError("解密需要 key")
        if use_nesh:
            return nexi_with_nesh_decrypt(data, key)
        else:
            return nexi_decrypt(data, key)

    raise TypeError("只接受 str 或 bytes")