import hashlib
import os
from nexi import nexi, nexi_decrypt, ALGO_TABLE, ALGO_NAMES

__version__ = "3.0.0"

# ===== Nesh 扩展 (BLAKE2b 哈希增强) =====

def nesh(data: bytes) -> bytes:
    """Nesh 哈希函数 —— 基于 BLAKE2b
    
    对数据生成 64 字节的确定性摘要，
    用于加密前的数据预处理或完整性校验。
    """
    h = hashlib.blake2b()
    h.update(data)
    return h.digest()


def nextxi_with_nesh(data: bytes, key: bytes) -> bytes:
    """加密 + Nesh 增强：先对明文做哈希混淆，再加密"""
    # 用 Nesh 哈希参与密钥扩展（而不是直接参与加密）
    h = hashlib.blake2b(key=key)
    h.update(data)
    derived_key = h.digest()[:4]  # 取前4字节作为派生密钥
    
    # 用派生密钥做加密
    out = bytearray()
    for i, b in enumerate(data):
        k = derived_key[i % 4]
        algo = ALGO_TABLE[i % len(ALGO_TABLE)]
        # _encrypt_byte from nexi
        from nexi import _encrypt_byte
        out.append(_encrypt_byte(b, k, algo))
    return bytes(out)


def nextxi_with_nesh_decrypt(data: bytes, key: bytes) -> bytes:
    """解密 + Nesh 增强：需要先重建派生密钥
    
    ⚠️ 注意：Nesh 增强模式下，解密需要知道原始明文的哈希来派生密钥，
    这意味着标准 Nesh 增强模式是单向的。
    实际解密请使用 nextxi(use_nesh=False) 模式。
    """
    raise NotImplementedError(
        "Nesh 增强模式是单向加密（哈希参与派生密钥），无法直接解密。"
        "如需可逆加密，请使用 nextxi(use_nesh=False)。"
    )


def nextxi(data, key=None, use_nesh=False, decrypt=False):
    """NextXi v3 统一接口 ✨

    Args:
        data:     要加密/解密的数据 (str 或 bytes)
        key:      密钥 (bytes)，默认随机生成 4 字节
        use_nesh: 是否启用 Nesh 哈希增强（单向加密，不可逆）
        decrypt:  True 为解密模式

    Returns:
        加密/解密后的 bytes
    """
    if isinstance(data, str):
        data = data.encode("utf-8")

    if key is None:
        key = os.urandom(4)

    if decrypt:
        if use_nesh:
            return nextxi_with_nesh_decrypt(data, key)
        else:
            return nexi_decrypt(data, key)
    else:
        if use_nesh:
            return nextxi_with_nesh(data, key)
        else:
            return nexi(data, key)
