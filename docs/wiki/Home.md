# 🏠 NextXi Wiki 首页

> 🔑 NextXi —— 轻量级多算法轮转加密引擎，专为 Python 设计

## 📖 目录

- [快速开始](./快速开始)
- [算法详解](./算法详解)
- [API 文档](./API文档)
- [更新日志](./更新日志)
- [常见问题](./常见问题)
- [贡献指南](./贡献指南)

## ✨ 项目简介

NextXi 是一个轻量级 Python 加密工具库，核心特色是**多算法轮转加密**——每个字节使用不同的加密算法，大幅提升安全性。

## 🔐 算法轮转

| 字节位置 | 算法名称 | 运算方式 |
|----------|----------|----------|
| 0 | Add（凯撒加法） | (b + k) & 0xFF |
| 1 | XOR（异或加密） | b ^ k |
| 2 | Rot（位旋转） | 循环左移 k 位 |
| 3 | NSwp（半字节交换+异或） | 高低4位互换再 ^ k |

4 种算法循环应用 → 攻击者破解一个字节不影响其他字节！

## 🚀 快速开始

```python
from nexi import nextxi

# 加密
key = b"\\x01\\x02\\x03\\x04"
encrypted = nextxi("Hello!", key=key)

# 解密
decrypted = nextxi(encrypted, key=key, decrypt=True)
print(decrypted.decode())  # Hello!
```

## 📊 版本历史

| 版本 | 亮点 |
|------|------|
| v1.0.0 | 基础凯撒加法加密 |
| v2.0.0 | Nesh 扩展 (BLAKE2b) |
| v3.0.0 | 🔥 多算法轮转加密 |

## 👤 作者

nomioe — [GitCode](https://gitcode.com/nomioe)

## 📜 许可证

MIT License
