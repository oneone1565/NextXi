import os

__version__ = "2.0.0"

# ===== 多算法定义 =====
# 每个位置使用不同算法，循环应用
ALGO_ADD   = 0  # 凯撒加法：(b + k) & 0xFF
ALGO_XOR   = 1  # 异或加密：b ^ k
ALGO_ROT   = 2  # 位旋转：循环左移 k 位
ALGO_NSWAP = 3  # 半字节交换 + 异或：高低4位互换再异或

# 算法轮转表 —— 按位置循环使用不同算法
ALGO_TABLE = [ALGO_ADD, ALGO_XOR, ALGO_ROT, ALGO_NSWAP]

ALGO_NAMES = {
    ALGO_ADD:   "Add  (加法)",
    ALGO_XOR:   "XOR  (异或)",
    ALGO_ROT:   "Rot  (位旋转)",
    ALGO_NSWAP: "NSwp (半字节交换+异或)",
}


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


def nexi(data: bytes, key: bytes) -> bytes:
    """多算法加密 🔐

    每个字节根据位置使用不同算法：
    - 位置 0: Add   (凯撒加法)
    - 位置 1: XOR   (异或)
    - 位置 2: Rot   (位旋转)
    - 位置 3: NSwp  (半字节交换+异或)
    然后循环，位置 4 又回到 Add ...
    """
    out = bytearray()
    for i, b in enumerate(data):
        k = key[i % len(key)]
        algo = ALGO_TABLE[i % len(ALGO_TABLE)]
        out.append(_encrypt_byte(b, k, algo))
    return bytes(out)


def nexi_decrypt(data: bytes, key: bytes) -> bytes:
    """多算法解密 🔓"""
    out = bytearray()
    for i, b in enumerate(data):
        k = key[i % len(key)]
        algo = ALGO_TABLE[i % len(ALGO_TABLE)]
        out.append(_decrypt_byte(b, k, algo))
    return bytes(out)


def nextxi(data, key=None, decrypt=False):
    """NextXi 统一接口

    Args:
        data: 要加密/解密的数据 (str 或 bytes)
        key:  密钥 (bytes)，默认随机生成 4 字节
        decrypt: True 为解密模式

    Returns:
        加密/解密后的 bytes
    """
    if isinstance(data, str):
        data = data.encode("utf-8")

    if key is None:
        key = os.urandom(4)

    if decrypt:
        return nexi_decrypt(data, key)
    else:
        return nexi(data, key)


def show_algo_plan(length: int) -> str:
    """展示前 N 个字节分别用什么算法（调试/教学用）"""
    lines = []
    for i in range(length):
        algo = ALGO_TABLE[i % len(ALGO_TABLE)]
        lines.append(f"  字节[{i:3d}]: {ALGO_NAMES[algo]}")
    return "\n".join(lines)
