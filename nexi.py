import os

__version__ = "3.0.0"
import random

# ===== 多算法定义 =====
ALGO_ADD   = 0  # 凯撒加法：(b + k) & 0xFF
ALGO_XOR   = 1  # 异或加密：b ^ k
ALGO_ROT   = 2  # 位旋转：循环左移 k 位
ALGO_NSWAP = 3  # 半字节交换 + 异或：高低4位互换再异或

ALL_ALGOS = [ALGO_ADD, ALGO_XOR, ALGO_ROT, ALGO_NSWAP]

def _gen_algo_table(seed_bytes: bytes = None) -> list:
    """🎲 根据种子生成随机算法轮转表
    
    每次加密随机打乱算法顺序，使每次加密使用的算法序列都不同！
    种子随密钥一起传递，解密时用相同种子还原顺序。
    """
    table = ALL_ALGOS[:]
    if seed_bytes:
        r = random.Random(seed_bytes)
        r.shuffle(table)
    else:
        random.shuffle(table)
    return table


def _rotl8(b: int, n: int) -> int:
    """8位循环左移"""
    n = n % 8
    return ((b << n) | (b >> (8 - n))) & 0xFF


def _rotr8(b: int, n: int) -> int:
    """8位循环右移"""
    n = n % 8
    return ((b >> n) | (b << (8 - n))) & 0xFF


def _nibble_swap(b: int) -> int:
    """交换高低4位 (nibble swap)"""
    return ((b << 4) | (b >> 4)) & 0xFF


def _encrypt_byte(b: int, k: int, algo: int) -> int:
    """用指定算法加密单个字节"""
    if algo == ALGO_ADD:
        return (b + k) & 0xFF
    elif algo == ALGO_XOR:
        return b ^ k
    elif algo == ALGO_ROT:
        return _rotl8(b, k % 8)
    elif algo == ALGO_NSWAP:
        return _nibble_swap(b) ^ k
    else:
        raise ValueError(f"未知算法编号: {algo}")


def _decrypt_byte(b: int, k: int, algo: int) -> int:
    """用指定算法解密单个字节（逆向操作）"""
    if algo == ALGO_ADD:
        return (b - k) & 0xFF
    elif algo == ALGO_XOR:
        return b ^ k  # 异或是自逆运算
    elif algo == ALGO_ROT:
        return _rotr8(b, k % 8)
    elif algo == ALGO_NSWAP:
        return _nibble_swap(b ^ k)  # 先异或再交换（逆序）
    else:
        raise ValueError(f"未知算法编号: {algo}")


def nexi(data: bytes, key: bytes, algo_table: list = None) -> bytes:
    """多算法随机轮转加密 🔐🎲

    每次加密随机打乱4种算法顺序！
    同样的明文+密钥，每次密文都不同！
    """
    if algo_table is None:
        algo_table = _gen_algo_table(key)
    out = bytearray()
    for i, b in enumerate(data):
        k = key[i % len(key)]
        algo = algo_table[i % len(algo_table)]
        out.append(_encrypt_byte(b, k, algo))
    return bytes(out)


def nexi_decrypt(data: bytes, key: bytes, algo_table: list = None) -> bytes:
    """多算法随机轮转解密 🔓"""
    if algo_table is None:
        algo_table = _gen_algo_table(key)
    out = bytearray()
    for i, b in enumerate(data):
        k = key[i % len(key)]
        algo = algo_table[i % len(algo_table)]
        out.append(_decrypt_byte(b, k, algo))
    return bytes(out)


def nextxi(data, key=None, decrypt=False, salt=None):
    """NextXi 统一接口 🎲

    Args:
        data:   要加密/解密的数据 (str 或 bytes)
        key:    密钥 (bytes)，默认随机生成 4 字节
        decrypt: True 为解密模式
        salt:   随机盐 (bytes)，加密时自动生成，解密时需传入
                每次加密用不同 salt → 算法顺序不同 → 密文不同！

    Returns:
        加密返回 (密文, salt) 元组；解密返回 bytes
    """
    if isinstance(data, str):
        data = data.encode("utf-8")

    if key is None:
        key = os.urandom(4)

    if decrypt:
        if salt is None:
            raise ValueError("解密需要提供加密时的 salt")
        algo_table = _gen_algo_table(key + salt)
        return nexi_decrypt(data, key, algo_table)
    else:
        if salt is None:
            salt = os.urandom(4)
        algo_table = _gen_algo_table(key + salt)
        encrypted = nexi(data, key, algo_table)
        return encrypted, salt


def show_algo_plan(length: int, algo_table: list = None) -> str:
    """展示算法轮转计划"""
    ALGO_NAMES = {0:"Add(加法)",1:"XOR(异或)",2:"Rot(位旋转)",3:"NSwp(半字节交换+异或)"}
    if algo_table is None:
        algo_table = _gen_algo_table()
    lines = [f"🎲 算法顺序: {' → '.join(ALGO_NAMES[a] for a in algo_table)}"]
    for i in range(length):
        algo = algo_table[i % len(algo_table)]
        lines.append(f"  字节[{i:3d}]: {ALGO_NAMES[algo]}")
    return "\n".join(lines)
