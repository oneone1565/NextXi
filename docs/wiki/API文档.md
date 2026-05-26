# 📚 API 文档

## nexi.py —— 核心加密模块 (v2.0)

### `nexi(data, key)`

多算法轮转加密。

**参数：**
| 参数 | 类型 | 说明 |
|------|------|------|
| data | bytes | 要加密的数据 |
| key | bytes | 密钥（建议 4 字节） |

**返回：** `bytes` — 加密后的数据

---

### `nexi_decrypt(data, key)`

多算法轮转解密。

**参数：** 同 `nexi()`

**返回：** `bytes` — 解密后的数据

---

### `nextxi(data, key=None, decrypt=False)`

统一加密/解密接口。

**参数：**
| 参数 | 类型 | 说明 |
|------|------|------|
| data | str 或 bytes | 要处理的数据 |
| key | bytes 或 None | 密钥，None 则随机生成 4 字节 |
| decrypt | bool | True 为解密模式 |

**返回：** `bytes`

**示例：**
```python
from nexi import nextxi

# 加密（str → bytes）
enc = nextxi("Hello", key=b"\\x01\\x02\\x03\\x04")

# 解密（bytes → bytes）
dec = nextxi(enc, key=b"\\x01\\x02\\x03\\x04", decrypt=True)
print(dec.decode())  # "Hello"
```

---

### `show_algo_plan(length)`

展示前 N 个字节的算法轮转计划（调试/教学用）。

**参数：**
| 参数 | 类型 | 说明 |
|------|------|------|
| length | int | 要展示的字节数 |

**返回：** `str` — 格式化的算法计划文本

---

## addon.py —— Nesh 扩展模块 (v3.0)

### `nesh(data)`

Nesh 哈希函数，基于 BLAKE2b。

**参数：**
| 参数 | 类型 | 说明 |
|------|------|------|
| data | bytes | 要哈希的数据 |

**返回：** `bytes` — 64 字节哈希摘要

---

### `nextxi(data, key=None, use_nesh=False, decrypt=False)`

带 Nesh 增强的统一接口。

**参数：**
| 参数 | 类型 | 说明 |
|------|------|------|
| data | str 或 bytes | 要处理的数据 |
| key | bytes 或 None | 密钥 |
| use_nesh | bool | 是否启用 Nesh 增强（单向加密） |
| decrypt | bool | True 为解密模式 |

**返回：** `bytes`

> ⚠️ `use_nesh=True` 时 `decrypt=True` 会抛出 `NotImplementedError`
